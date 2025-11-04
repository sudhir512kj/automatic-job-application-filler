#!/usr/bin/env python3
"""
Test script to verify form filling improvements
"""

import asyncio
from backend.services.form_filler import FormFiller

async def test_form_filler():
    """Test the form filler with sample data"""
    
    # Sample resume data (similar to what you're getting)
    sample_resume_data = {
        'Full Name': 'Sudhir Meena',
        'Email': 'sudhirmeena230995@gmail.com',
        'Phone Number': '7850905317',
        'Address': 'Gurugram, Haryana, India',
        'Education': 'Bachelor of Technology in Computer Science',
        'Work Experience': 'Senior Associate Technology L1 at Publicis Groupe (10/2025 - current), Lead Software Engineer at Persistent Systems (07/2023 - 09/2025)',
        'Skills': 'Java, Spring Boot, AWS, Azure, Golang, Kubernetes, Python, React, MongoDB, microservices architecture'
    }
    
    # Sample form fields (similar to what you're getting)
    sample_form_fields = {
        'fields': [
            {'type': 'text', 'label': 'Name', 'required': False, 'options': []},
            {'type': 'textarea', 'label': 'Skills', 'required': False, 'options': []},
            {'type': 'text', 'label': 'Education', 'required': False, 'options': []},
            {'type': 'text', 'label': 'Email', 'required': False, 'options': []},
            {'type': 'text', 'label': 'Phone Number', 'required': False, 'options': []},
        ],
        'mappings': {}
    }
    
    print("Testing form filler with sample data...")
    print(f"Resume data keys: {list(sample_resume_data.keys())}")
    print(f"Form fields: {len(sample_form_fields['fields'])}")
    
    # Test data mapping logic
    filler = FormFiller()
    data_map = filler._prepare_data_mapping(sample_resume_data)
    print(f"Data mapping: {data_map}")
    
    # Test smart value matching
    test_contexts = ['name', 'email', 'phone number', 'skills', 'education']
    for context in test_contexts:
        value = filler._get_smart_value(context, data_map)
        print(f"Context '{context}' -> Value: {value[:50] if value else 'None'}")

if __name__ == "__main__":
    asyncio.run(test_form_filler())