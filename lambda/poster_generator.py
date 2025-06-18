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

def generate_poster_prompt():
    """Generate a creative prompt for the safety poster."""
    tip = random.choice(SAFETY_TIPS)
    style = random.choice(POSTER_STYLES)
    scenario = random.choice(SHRIMP_SCENARIOS)
    
    prompt = f"""Create a {style} featuring {scenario}. 
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
        
        # Generate the poster prompt
        prompt, safety_tip = generate_poster_prompt()
        logger.info(f"Generated prompt for tip: {safety_tip}")
        
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