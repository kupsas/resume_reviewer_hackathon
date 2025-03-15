import pytest
import os
from dotenv import load_dotenv
import openai

load_dotenv()

def test_openai_api_key():
    """Test that OpenAI API key is configured and working."""
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OpenAI API key not found in environment variables"
    
    try:
        # Initialize the client
        client = openai.OpenAI(api_key=api_key)
        
        # Make a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=10
        )
        
        assert response is not None
        assert response.choices[0].message.content is not None
        
    except Exception as e:
        pytest.fail(f"OpenAI API call failed: {str(e)}") 