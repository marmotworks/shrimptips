from lambdas.web_interface import lambda_handler

def test_lambda_handler_root():
    event = {'path': '/'}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert 'text/html' in response['headers']['Content-Type']
    assert '🦐 ShrimpTips' in response['body']

def test_lambda_handler_api_poster_404():
    event = {'path': '/api/poster'}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404
    assert 'Poster API endpoint not found' in response['body']

def test_lambda_handler_default_path():
    event = {} # path missing
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert '🦐 ShrimpTips' in response['body']
