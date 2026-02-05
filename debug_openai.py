"""
Debug script to understand OpenAI library issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import openai
    print(f"OpenAI version: {openai.__version__}")
    print(f"OpenAI module location: {openai.__file__}")

    # Check OpenAI client class
    print(f"OpenAI client class: {openai.OpenAI}")

    # Check constructor signature
    import inspect
    sig = inspect.signature(openai.OpenAI.__init__)
    print(f"OpenAI.__init__ signature: {sig}")

    # Try to create client with minimal params
    try:
        client = openai.OpenAI(api_key="test")
        print("✓ OpenAI client created successfully with api_key only")
    except Exception as e:
        print(f"✗ Failed to create OpenAI client: {e}")

    # Check if proxies parameter exists
    params = list(sig.parameters.keys())
    print(f"Available parameters: {params}")

    if 'proxies' in params:
        print("⚠ 'proxies' parameter is available")
    else:
        print("✓ 'proxies' parameter is NOT available (good)")

except ImportError as e:
    print(f"Failed to import openai: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
