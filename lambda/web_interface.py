"""
Lambda function to serve the web interface for ShrimpTips.
"""
import json
import boto3

def lambda_handler(event, context):
    """
    Serve the HTML interface for the ShrimpTips webapp.
    """
    
    # Check if this is a request for the poster API
    path = event.get('path', '/')
    
    if path == '/api/poster':
        # This should be handled by the poster_generator function
        return {
            'statusCode': 404,
            'body': 'Poster API endpoint not found'
        }
    
    # Serve the main HTML page
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShrimpTips - Ocean Safety for Wild Shrimp</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 3em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            color: #FFD700;
        }
        
        .header p {
            font-size: 1.2em;
            margin: 10px 0;
            opacity: 0.9;
        }
        
        .poster-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 90%;
            text-align: center;
        }
        
        .poster-image {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .loading {
            color: #333;
            font-size: 1.1em;
            padding: 40px;
        }
        
        .error {
            color: #d32f2f;
            font-size: 1.1em;
            padding: 40px;
        }
        
        .generate-btn {
            background: #FF6B35;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.1em;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 20px;
            transition: background 0.3s ease;
        }
        
        .generate-btn:hover {
            background: #E55A2B;
        }
        
        .generate-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .safety-tip {
            color: #333;
            font-weight: bold;
            font-size: 1.2em;
            margin-top: 15px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            opacity: 0.7;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🦐 ShrimpTips</h1>
        <p>Ocean Safety & Health Guidance for Wild Shrimp</p>
        <p><em>Professional Safety Posters by the Ocean Floor Safety Inspectors Union</em></p>
    </div>
    
    <div class="poster-container">
        <div id="poster-content">
            <div class="loading">
                🌊 Generating your personalized shrimp safety poster...<br>
                <small>This may take a few moments</small>
            </div>
        </div>
        <button id="generate-btn" class="generate-btn" onclick="generateNewPoster()" disabled>
            Generate New Poster
        </button>
    </div>
    
    <div class="footer">
        <p>Powered by AWS Bedrock Nova Canvas | Keeping our crustacean friends safe since 2024</p>
    </div>

    <script>
        let isGenerating = false;
        
        async function generatePoster() {
            if (isGenerating) return;
            
            isGenerating = true;
            const btn = document.getElementById('generate-btn');
            const content = document.getElementById('poster-content');
            
            btn.disabled = true;
            btn.textContent = 'Generating...';
            
            content.innerHTML = '<div class="loading">🌊 Generating your personalized shrimp safety poster...<br><small>This may take a few moments</small></div>';
            
            try {
                const response = await fetch('/api/poster', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.message || 'Unknown error occurred');
                }
                
                // Display the generated poster
                content.innerHTML = `
                    <img src="data:image/png;base64,${data.image}" alt="Shrimp Safety Poster" class="poster-image">
                    <div class="safety-tip">"${data.safety_tip}"</div>
                `;
                
            } catch (error) {
                console.error('Error generating poster:', error);
                content.innerHTML = `
                    <div class="error">
                        ⚠️ Oops! Something went wrong generating your poster.<br>
                        <small>${error.message}</small><br>
                        <small>Please try again in a moment.</small>
                    </div>
                `;
            } finally {
                isGenerating = false;
                btn.disabled = false;
                btn.textContent = 'Generate New Poster';
            }
        }
        
        function generateNewPoster() {
            generatePoster();
        }
        
        // Generate initial poster when page loads
        window.addEventListener('load', function() {
            setTimeout(generatePoster, 1000);
        });
    </script>
</body>
</html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        },
        'body': html_content
    }
