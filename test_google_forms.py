#!/usr/bin/env python3
"""
Test Google Forms service
"""

import asyncio
import sys
sys.path.append('/Users/sudhirmeena/auto-form-filling-agent/backend')

from dotenv import load_dotenv
load_dotenv('/Users/sudhirmeena/auto-form-filling-agent/backend/.env')

from services.google_forms_service import GoogleFormsService

async def test_google_forms():
    """Test Google Forms service"""
    
    print("🧪 Testing Google Forms Service")
    print("=" * 40)
    
    service = GoogleFormsService()
    
    # Test form ID extraction
    test_url = "https://docs.google.com/forms/d/e/1FAIpQLSeJEyE-iAV3w7b8pXbBPxrfIw3elepy9kkJL6Av0DBpTsQbaQ/viewform"
    form_id = service.extract_form_id(test_url)
    print(f"✅ Form ID extracted: {form_id}")
    
    # Test form structure analysis
    try:
        structure = await service.get_form_structure(test_url)
        print(f"✅ Form structure: {len(structure['fields'])} fields detected")
        for field in structure['fields'][:3]:  # Show first 3 fields
            print(f"   - {field.get('label', 'Unknown')}: {field.get('type', 'text')}")
    except Exception as e:
        print(f"❌ Form structure analysis failed: {e}")
    
    # Test resume mapping
    sample_resume = {
        'Full Name': 'John Doe',
        'Email': 'john@example.com',
        'Phone Number': '123-456-7890',
        'Skills': 'Python, JavaScript, React'
    }
    
    try:
        result = await service.submit_form_response(test_url, sample_resume)
        print(f"✅ Form submission result: {result.get('success', False)}")
        if result.get('filled_fields'):
            print(f"   Filled {len(result['filled_fields'])} fields")
    except Exception as e:
        print(f"❌ Form submission test failed: {e}")
    
    print("\n🎯 Benefits of Google Forms Service:")
    print("- No Selenium/browser automation needed")
    print("- Direct API-based form submission")
    print("- AI-powered field mapping")
    print("- Faster and more reliable")

if __name__ == "__main__":
    asyncio.run(test_google_forms())