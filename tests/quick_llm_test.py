#!/usr/bin/env python3
"""
Quick test to identify LLM response truncation issue
"""
import requests
import json

def test_ollama_direct():
    """Test direct Ollama call with minimal setup"""
    print("🔍 Testing Ollama directly...")
    
    # Simple test request
    request_data = {
        "model": "devstral:latest",
        "prompt": "What planet are we on?",
        "stream": False,
        "options": {
            "num_predict": 100,  # Allow 100 tokens for response
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate", 
            json=request_data, 
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                response_text = result.get("response", "")
                print(f"Response length: {len(response_text)} chars")
                print(f"Response: '{response_text}'")
                
                # Check for common truncation indicators
                if len(response_text.strip()) < 5:
                    print("❌ ISSUE: Response is too short!")
                elif response_text.strip() in ["Ah", "I", "The", "We"]:
                    print("❌ ISSUE: Response appears truncated to single word!")
                else:
                    print("✅ Response looks normal")
                    
                # Check response metadata
                print(f"Done: {result.get('done', 'unknown')}")
                print(f"Total duration: {result.get('total_duration', 'unknown')}")
                print(f"Load duration: {result.get('load_duration', 'unknown')}")
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON error: {e}")
                print(f"Raw response: {response.text[:200]}...")
        else:
            print(f"❌ HTTP error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_with_longer_response():
    """Test with request that should generate longer response"""
    print("\n🔍 Testing with longer response request...")
    
    request_data = {
        "model": "devstral:latest", 
        "prompt": "What planet are we on? Please explain in detail about Earth, including its position in the solar system, its characteristics, and why it's suitable for life.",
        "stream": False,
        "options": {
            "num_predict": 500,  # Allow more tokens
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=request_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            print(f"Longer response length: {len(response_text)} chars")
            print(f"First 200 chars: '{response_text[:200]}...'")
            
            if len(response_text.strip()) < 20:
                print("❌ ISSUE: Even detailed request gives short response!")
            else:
                print("✅ Longer request works fine")
        else:
            print(f"❌ HTTP error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def check_model_info():
    """Check if model is loaded and working"""
    print("\n🔍 Checking model info...")
    
    try:
        # Check if model is loaded
        response = requests.get("http://localhost:11434/api/ps", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"Loaded models: {models}")
        
        # Get model info
        response = requests.post(
            "http://localhost:11434/api/show",
            json={"name": "devstral:latest"},
            timeout=10
        )
        if response.status_code == 200:
            info = response.json()
            print(f"Model info available: {bool(info)}")
            if 'parameters' in info:
                print(f"Model parameters: {info.get('parameters', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Model check error: {e}")

if __name__ == "__main__":
    print("🚀 Quick LLM Truncation Test\n")
    
    check_model_info()
    test_ollama_direct()
    test_with_longer_response()
    
    print("\n✅ Test complete!")