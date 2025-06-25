"""
Tests for the web interface lambda function.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from web_interface import lambda_handler


def test_web_interface_capitalization():
    """
    Test that the web interface has proper capitalization for text elements.
    """
    # Mock event and context
    event = {'path': '/'}
    context = {}

    # Call the lambda handler
    response = lambda_handler(event, context)

    # Check that the response is successful
    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'text/html'

    # Get the HTML content
    html_content = response['body']

    # Check for proper capitalization of "Professional Safety Posters"
    assert 'Professional Safety Posters by the Ocean Floor Safety Inspectors Union' in html_content

    # Ensure the old incorrect capitalization is not present
    assert 'Professional safety posters by the Ocean Floor Safety Inspectors Union' not in html_content

    print("✅ Capitalization test passed!")


def test_web_interface_basic_structure():
    """
    Test that the web interface returns the expected HTML structure.
    """
    # Mock event and context
    event = {'path': '/'}
    context = {}

    # Call the lambda handler
    response = lambda_handler(event, context)

    # Check that the response is successful
    assert response['statusCode'] == 200

    # Get the HTML content
    html_content = response['body']

    # Check for key elements
    assert '<!DOCTYPE html>' in html_content
    assert '<title>ShrimpTips - Ocean Safety for Wild Shrimp</title>' in html_content
    assert '🦐 ShrimpTips' in html_content
    assert 'Ocean Safety & Health Guidance for Wild Shrimp' in html_content
    assert 'Generate New Poster' in html_content

    print("✅ Basic structure test passed!")


def test_api_poster_endpoint():
    """
    Test that the API poster endpoint returns 404 as expected.
    """
    # Mock event and context for API endpoint
    event = {'path': '/api/poster'}
    context = {}

    # Call the lambda handler
    response = lambda_handler(event, context)

    # Check that it returns 404 for the poster API endpoint
    assert response['statusCode'] == 404
    assert 'Poster API endpoint not found' in response['body']

    print("✅ API endpoint test passed!")


if __name__ == '__main__':
    test_web_interface_capitalization()
    test_web_interface_basic_structure()
    test_api_poster_endpoint()
    print("🎉 All tests passed!")
