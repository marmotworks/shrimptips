from lambdas.web_interface import lambda_handler

def test_lambda_handler_root():
    event = {'path': '/'}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert 'text/html' in response['headers']['Content-Type']
    assert '🦐 ShrimpTips' in response['body']

def test_lambda_handler_default_path():
    event = {} # path missing
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert '🦐 ShrimpTips' in response['body']

def test_lambda_handler_contains_poster_elements():
    event = {'path': '/'}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    body = response['body']
    assert 'poster-content' in body
    assert 'poster-image' in body
    assert 'safety-tip' in body
    assert 'generate-btn' in body
    assert 'api/poster' in body
