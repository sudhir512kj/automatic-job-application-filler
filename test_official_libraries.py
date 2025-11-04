#!/usr/bin/env python3
"""
Test official AI libraries integration
"""

import asyncio
import os
import sys
sys.path.append('/Users/sudhirmeena/auto-form-filling-agent/backend')

from dotenv import load_dotenv
load_dotenv('/Users/sudhirmeena/auto-form-filling-agent/backend/.env')

from services.resume_parser import ResumeParser

async def test_official_libraries():
    """Test official libraries"""
    
    print("🧪 Testing Official AI Libraries Integration")
    print("=" * 50)
    
    # Test OpenRouter LLM
    try:
        parser = ResumeParser()
        if parser.llm:
            print("✅ OpenRouter LLM initialized successfully")
            
            # Test simple completion
            sample_text = "John Doe\nEmail: john@example.com\nPhone: 123-456-7890\nSkills: Python, Java"
            result = await parser._parse_with_ai(sample_text)
            print(f"✅ OpenRouter parsing result: {result.get('Full Name', 'No name')}")
        else:
            print("❌ OpenRouter LLM not initialized")
    except Exception as e:
        print(f"❌ OpenRouter test failed: {e}")
    
    # Test LlamaParse
    try:
        if parser.parser:
            print("✅ LlamaParse initialized successfully")
        else:
            print("❌ LlamaParse not initialized")
    except Exception as e:
        print(f"❌ LlamaParse test failed: {e}")
    
    print("\n🎯 Summary:")
    print("- Using llama-index-llms-openrouter for OpenRouter")
    print("- Using llama-parse for document parsing")
    print("- No direct API calls - all through official libraries")

if __name__ == "__main__":
    asyncio.run(test_official_libraries())