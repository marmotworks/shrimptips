"""
Lambda function to generate OSHA-style safety posters for wild shrimp using AWS Bedrock Nova Canvas.
"""
import json
import base64
import boto3
import random
from botocore.config import Config

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1',
    config=Config(read_timeout=300)
)

# Shrimp safety tips and themes
SAFETY_TIPS = [
    "Beware the Bottom Trawlers!",
    "Current Awareness is Self-Awareness",
    "Stay Alert in Kelp Forests",
    "Predator Detection Saves Lives",
    "Pollution Zones: Know Before You Go",
    "Deep Water Safety First",
    "Maintain Your Exoskeleton",
    "School Together, Stay Safe Together",
    "Temperature Changes: Adapt or Perish",
    "Oxygen Levels Matter",
    "Avoid Plastic Debris",
    "Know Your Escape Routes",
    "Camouflage is Your Friend",
    "Night Swimming Precautions",
    "Spawning Season Safety"
]

POSTER_STYLES = [
    "vintage 1950s OSHA safety poster style",
    "retro industrial safety poster with bold typography",
    "classic workplace safety poster design",
    "vintage public service announcement poster",
    "mid-century modern safety poster aesthetic"
]

SHRIMP_SCENARIOS = [
    "wild shrimp in ocean environment",
    "marine shrimp avoiding fishing nets",
    "ocean floor dwelling shrimp",
    "shrimp in coral reef habitat",
    "deep sea shrimp in dark waters",
    "coastal shrimp in shallow waters",
    "shrimp school swimming together",
    "shrimp hiding in seaweed"
]

def generate_creative_prompt_with_ai():
    """Use Bedrock Nova Pro to generate a creative and varied poster prompt."""
    
    # Create a prompt for the AI to generate a poster description
    ai_prompt = """You are a creative director for the Ocean Floor Safety Inspectors Union, tasked with creating OSHA-style safety posters for wild shrimp. 

Generate a unique and creative safety poster concept that includes:
1. A specific safety tip or warning for wild shrimp (be creative but realistic to ocean dangers)
2. A visual scenario description featuring shrimp in their ocean environment
3. Specific visual style elements that would work for a vintage OSHA poster

Your response should be a detailed image generation prompt that includes:
- The safety message/slogan (make it catchy and memorable)
- The visual scene (specific ocean environment, shrimp behavior, potential hazards)
- Visual style (vintage OSHA poster aesthetic with maritime elements)
- Color scheme and typography suggestions
- Safety symbols and iconography to include

Be creative and vary the scenarios - think about different ocean zones (coral reefs, deep sea, kelp forests, open ocean), different types of hazards (predators, pollution, fishing equipment, currents, temperature changes), and different shrimp behaviors (schooling, feeding, hiding, migrating).

Format your response as a single detailed image generation prompt, and end with the safety slogan in quotes."""

    try:
        # Call Nova Pro to generate the creative prompt
        request_body = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": ai_prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 500,
                "temperature": 0.8,
                "topP": 0.9
            }
        })
        
        response = bedrock.invoke_model(
            body=request_body,
            modelId='amazon.nova-pro-v1:0',
            accept='application/json',
            contentType='application/json'
        )
        
        response_json = json.loads(response.get("body").read())
        generated_content = response_json['output']['message']['content'][0]['text']
        
        # Extract the safety slogan from the end of the response
        lines = generated_content.strip().split('\n')
        safety_tip = "Stay Safe in the Deep Blue!"  # Default fallback
        
        # Look for quoted text at the end which should be our safety slogan
        for line in reversed(lines):
            if '"' in line:
                # Extract text between quotes
                import re
                quotes = re.findall(r'"([^"]*)"', line)
                if quotes:
                    safety_tip = quotes[-1]
                    break
        
        return generated_content.strip(), safety_tip
        
    except Exception as e:
        # Fallback to original method if AI generation fails
        import logging
        logger = logging.getLogger()
        logger.warning(f"AI prompt generation failed, falling back to original method: {str(e)}")
        return generate_fallback_prompt()

def generate_fallback_prompt():
    """Fallback method using the original approach with some enhancements."""
    tip = random.choice(SAFETY_TIPS)
    style = random.choice(POSTER_STYLES)
    scenario = random.choice(SHRIMP_SCENARIOS)
    
    # Add some additional creative elements
    additional_elements = [
        "with dramatic lighting and shadows",
        "featuring bold warning triangles and exclamation marks",
        "with a weathered, vintage texture",
        "including maritime safety symbols and anchors",
        "with a distressed paper background effect",
        "featuring classic OSHA color combinations"
    ]
    
    extra_element = random.choice(additional_elements)
    
    prompt = f"""Create a {style} featuring {scenario} {extra_element}. 
    The poster should have the safety message "{tip}" prominently displayed in bold, readable text.
    Include OSHA-style warning symbols and safety iconography.
    Use a color scheme typical of vintage safety posters (yellows, reds, blacks).
    The overall design should be professional yet slightly whimsical, 
    as if created by a union of ocean-floor safety inspectors.
    Include maritime safety elements and ocean-themed warning symbols.
    Make it look like an official workplace safety poster but for marine life."""
    
    return prompt, tip

def lambda_handler(event, context):
    """
    Main Lambda handler function.
    """
    try:
        import logging
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.info("Starting poster generation")
        
        # Generate the poster prompt using AI
        prompt, safety_tip = generate_creative_prompt_with_ai()
        logger.info(f"Generated AI prompt for tip: {safety_tip}")
        logger.info(f"Full prompt: {prompt[:200]}...")  # Log first 200 chars for debugging
        
        # Prepare the request body for Nova Canvas
        api_request = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
                "negativeText": "blurry, low quality, distorted text, unreadable, modern digital style"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 1024,
                "width": 768,  # Portrait orientation for poster
                "seed": random.randint(1, 1000000),
                "cfgScale": 7.0,
                "quality": "premium"
            }
        })
        
        logger.info("Calling Bedrock Nova Canvas")
        
        # Call Nova Canvas to generate the image
        response = bedrock.invoke_model(
            body=api_request,
            modelId='amazon.nova-canvas-v1:0',
            accept='application/json',
            contentType='application/json'
        )
        
        logger.info("Received response from Bedrock")
        
        # Parse the response
        response_json = json.loads(response.get("body").read())
        base64_image = response_json.get("images")[0]
        
        logger.info("Successfully generated poster image")
        
        # Return the image as base64 with metadata
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'image': base64_image,
                'safety_tip': safety_tip,
                'prompt_used': prompt
            })
        }
        
    except Exception as e:
        logger.error(f"Error generating poster: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Failed to generate poster',
                'message': str(e),
                'error_type': type(e).__name__
            })
        }