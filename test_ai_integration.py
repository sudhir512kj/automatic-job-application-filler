#!/usr/bin/env python3
"""
Test AI integration for form filling
"""

import asyncio
import os
import sys
sys.path.append('/Users/sudhirmeena/auto-form-filling-agent/backend')

from dotenv import load_dotenv
load_dotenv('/Users/sudhirmeena/auto-form-filling-agent/backend/.env')

from services.resume_parser import ResumeParser
import httpx
from config import FREE_MODELS, OPENROUTER_BASE_URL, REQUIRED_HEADERS

async def test_ai_integration():
    """Test AI integration"""
    
    # Test OpenRouter API connection
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    print("✅ OpenRouter API key found")
    
    # Test simple API call
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENROUTER_BASE_URL,
                headers={
                    "Authorization": f"Bearer {openrouter_key}",
                    "Content-Type": "application/json",
                    **REQUIRED_HEADERS
                },
                json={
                    "model": FREE_MODELS["primary"],
                    "messages": [{"role": "user", "content": "Hello, respond with 'AI working'"}],
                    "max_tokens": 10
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"✅ OpenRouter API working: {content}")
            else:
                print(f"❌ OpenRouter API failed: {response.status_code}")
                
    except Exception as e:
        print(f"❌ OpenRouter API error: {e}")
    
    # Test Llama Cloud API
    llama_key = os.getenv("LLAMA_CLOUD_API_KEY")
    if llama_key:
        print("✅ Llama Cloud API key found")
    else:
        print("❌ LLAMA_CLOUD_API_KEY not found")
    
    # Test resume parser
    try:
        parser = ResumeParser()
        sample_text = "John Doe\nEmail: john@example.com\nPhone: 123-456-7890\nSkills: Python, Java"
        result = await parser._parse_with_ai(sample_text)
        print(f"✅ Resume parser working: {result.get('Full Name', 'No name')}")
    except Exception as e:
        print(f"❌ Resume parser error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_integration())