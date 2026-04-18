from unittest.mock import MagicMock, patch
from lambdas.poster_generator import lambda_handler, generate_fallback_prompt

@patch('lambdas.poster_generator.bedrock')
def test_lambda_handler_success(mock_bedrock):
    # Mock Nova Pro response for prompt generation
    mock_pro_response = MagicMock()
    mock_pro_response.get.return_value = MagicMock()
    mock_pro_response.get("body").read.return_value = b'{"output": {"message": {"content": [{"text": "A vintage poster of a shrimp. \\"Stay Safe!\\""}]}}}'
    
    # Mock Nova Canvas response for image generation
    mock_nova_response = MagicMock()
    mock_nova_response.get.return_value = MagicMock()
    mock_nova_response.get("body").read.return_value = b'{"images": [{"format": "png", "data": "base64_image_data"}]}'

    mock_bedrock.invoke_model.side_effect = [mock_pro_response, mock_nova_response]
    
    response = lambda_handler({}, None)
    
    assert response['statusCode'] == 200
    import json
    body = json.loads(response['body'])
    assert body['image'] == "base64_image_data"
    assert body['safety_tip'] == "Stay Safe!"

@patch('lambdas.poster_generator.bedrock')
def test_lambda_handler_failure(mock_bedrock):
    mock_bedrock.invoke_model.side_effect = Exception("Bedrock Error")
    
    response = lambda_handler({}, None)
    assert response['statusCode'] == 500
    import json
    body = json.loads(response['body'])
    assert body['error'] == "Failed to generate poster"

def test_generate_fallback_prompt():
    prompt, tip = generate_fallback_prompt()
    assert isinstance(prompt, str)
    assert isinstance(tip, str)
    assert len(prompt) > 0
    assert len(tip) > 0
