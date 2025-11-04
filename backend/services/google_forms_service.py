import os
import json
import requests
import re
from urllib.parse import quote
from logger import log_error
from llama_index.llms.openrouter import OpenRouter

class GoogleFormsService:
    ALL_DATA_FIELDS = "FB_PUBLIC_LOAD_DATA_"
    
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.form_data = None
        self.entries = None
        
        # Initialize OpenRouter LLM for field mapping
        if self.openrouter_key:
            self.llm = OpenRouter(
                api_key=self.openrouter_key,
                model="mistralai/mistral-7b-instruct:free",
                max_tokens=1000,
                temperature=0.1
            )
        

    
    def extract_form_id(self, form_url: str) -> str:
        """Extract form ID from Google Forms URL"""
        try:
            if '/forms/d/e/' in form_url:
                form_id = form_url.split('/forms/d/e/')[1].split('/')[0]
                return form_id
            elif '/forms/d/' in form_url:
                form_id = form_url.split('/forms/d/')[1].split('/')[0]
                return form_id
            else:
                raise ValueError("Invalid Google Forms URL")
        except Exception as e:
            log_error(f"Failed to extract form ID: {e}", "google-forms")
            return None
    
    async def get_form_structure(self, form_url: str) -> dict:
        """Get form structure"""
        form_id = self.extract_form_id(form_url)
        return {"fields": self._get_default_fields(), "form_id": form_id}
    

    
    def _get_default_fields(self) -> list:
        """Return default form fields"""
        return [
            {"type": "text", "label": "Name"},
            {"type": "email", "label": "Email"},
            {"type": "text", "label": "Phone"},
            {"type": "textarea", "label": "Skills"},
            {"type": "text", "label": "Education"}
        ]
    
    async def submit_form_response(self, form_url: str, resume_data: dict) -> dict:
        """Submit form response using reference repo approach"""
        try:
            # Parse form entries from the URL
            entries = self._parse_form_entries(form_url)
            if not entries:
                return {"success": False, "error": "Could not parse form entries"}
            
            # Fill entries with resume data
            filled_data = self._fill_entries_with_resume_data(entries, resume_data)
            
            # Submit the form
            success = self._submit_form(form_url, filled_data)
            
            if success:
                return {
                    "success": True,
                    "filled_fields": [f"{k}: {str(v)[:50]}..." for k, v in filled_data.items()],
                    "message": f"Form submitted successfully with {len(filled_data)} fields"
                }
            else:
                return {"success": False, "error": "Form submission failed"}
                    
        except Exception as e:
            log_error(f"Form submission failed: {e}", "google-forms")
            return {"success": False, "error": str(e)}
    

    
    def _get_form_response_url(self, url: str) -> str:
        """Convert form URL to form response URL"""
        url = url.replace('/viewform', '/formResponse')
        if not url.endswith('/formResponse'):
            if not url.endswith('/'):
                url += '/'
            url += 'formResponse'
        return url
    
    def _extract_script_variables(self, name: str, html: str):
        """Extract a variable from a script tag in a HTML page"""
        pattern = re.compile(r'var\s' + name + r'\s=\s(.*?);')
        match = pattern.search(html)
        if not match:
            return None
        value_str = match.group(1)
        return json.loads(value_str)
    
    def _get_fb_public_load_data(self, url: str):
        """Get form data from a Google form URL"""
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            log_error(f"Can't get form data: {response.status_code}", "google-forms")
            return None
        return self._extract_script_variables(self.ALL_DATA_FIELDS, response.text)
    
    def _parse_form_entries(self, url: str):
        """Parse the form entries and return a list of entries"""
        self.form_data = self._get_fb_public_load_data(url)
        
        if not self.form_data or not self.form_data[1] or not self.form_data[1][1]:
            log_error("Can't get form entries", "google-forms")
            return None
        
        parsed_entries = []
        for entry in self.form_data[1][1]:
            if entry[3] == 8:  # Skip session type entries
                continue
            
            entry_name = entry[1]
            for sub_entry in entry[4]:
                info = {
                    "id": sub_entry[0],
                    "name": entry_name,
                    "type": entry[3],
                    "required": sub_entry[2] == 1,
                    "options": [x[0] for x in sub_entry[1]] if sub_entry[1] else None,
                }
                parsed_entries.append(info)
        
        return parsed_entries
    
    def _fill_entries_with_resume_data(self, entries, resume_data):
        """Fill form entries with resume data"""
        filled_data = {}
        
        for entry in entries:
            entry_id = f"entry.{entry['id']}"
            entry_name = entry['name'].lower()
            
            value = None
            if any(word in entry_name for word in ['name', 'full name']):
                value = resume_data.get('Full Name')
            elif any(word in entry_name for word in ['email', 'mail']):
                value = resume_data.get('Email')
            elif any(word in entry_name for word in ['phone', 'mobile', 'contact']):
                value = resume_data.get('Phone Number')
            elif any(word in entry_name for word in ['skill', 'technology']):
                value = resume_data.get('Skills')
            elif any(word in entry_name for word in ['education', 'degree']):
                value = resume_data.get('Education')
            elif any(word in entry_name for word in ['experience', 'work', 'job']):
                value = resume_data.get('Work Experience')
            
            if value:
                filled_data[entry_id] = str(value)
        
        return filled_data
    
    def _submit_form(self, url: str, data: dict) -> bool:
        """Submit the form with data"""
        submit_url = self._get_form_response_url(url)
        
        try:
            response = requests.post(submit_url, data=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            log_error(f"Form submission error: {e}", "google-forms")
            return False
    
    def _map_question_to_resume(self, title: str, resume_data: dict) -> str:
        """Map form question to resume data"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['name', 'full name']):
            return resume_data.get('Full Name', '')
        elif any(word in title_lower for word in ['email', 'mail']):
            return resume_data.get('Email', '')
        elif any(word in title_lower for word in ['phone', 'mobile', 'contact']):
            return resume_data.get('Phone Number', '')
        elif any(word in title_lower for word in ['skill', 'technology']):
            return resume_data.get('Skills', '')
        elif any(word in title_lower for word in ['education', 'degree']):
            return resume_data.get('Education', '')
        elif any(word in title_lower for word in ['experience', 'work', 'job']):
            return resume_data.get('Work Experience', '')
        
        return ''
    
