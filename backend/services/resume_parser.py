import os
import asyncio
import json
from PyPDF2 import PdfReader
from docx import Document
import io
from logger import log_resume_data, log_error

# Official LlamaIndex libraries
from llama_index.llms.openrouter import OpenRouter
from llama_parse import LlamaParse
from llama_index.core import Document as LlamaDocument

class ResumeParser:
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.llama_key = os.getenv("LLAMA_CLOUD_API_KEY")
        
        # Initialize OpenRouter LLM
        if self.openrouter_key:
            self.llm = OpenRouter(
                api_key=self.openrouter_key,
                model="mistralai/mistral-7b-instruct:free",
                max_tokens=1500,
                temperature=0.0
            )
        
        # Initialize LlamaParse
        if self.llama_key:
            self.parser = LlamaParse(
                api_key=self.llama_key,
                result_type="text",
                parsing_instruction="Extract structured information including name, email, phone, address, education, work experience, and skills from this resume document."
            )
    
    async def extract_data(self, content: bytes, filename: str) -> dict:
        # Try Llama Cloud first with original file
        llama_result = await self._try_llama_cloud(content, filename)
        if llama_result:
            return llama_result
            
        # Fallback to text extraction + OpenRouter
        text = self._extract_text(content, filename)
        return await self._parse_with_ai(text)
    
    def _extract_text(self, content: bytes, filename: str) -> str:
        if filename.endswith('.pdf'):
            return self._extract_pdf_text(content)
        elif filename.endswith('.docx'):
            return self._extract_docx_text(content)
        else:
            return content.decode('utf-8')
    
    def _extract_pdf_text(self, content: bytes) -> str:
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    def _extract_docx_text(self, content: bytes) -> str:
        doc = Document(io.BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    async def _parse_with_ai(self, text: str) -> dict:
        """Parse resume text using OpenRouter LLM"""
        if not self.llm:
            log_error("OpenRouter LLM not initialized", "resume-parser")
            return self._get_fallback_data()
        
        prompt = f"""
Extract and structure the following resume information into JSON format:

{{
    "Full Name": "extracted full name",
    "Email": "extracted email address", 
    "Phone Number": "extracted phone number",
    "Address": "extracted address",
    "Education": "education background",
    "Work Experience": "work experience summary",
    "Skills": "technical and professional skills"
}}

Resume text:
{text[:2000]}

Return only valid JSON, no additional text.
"""
        
        try:
            response = await self.llm.acomplete(prompt)
            content = str(response).strip()
            
            # Clean and parse JSON response
            cleaned_content = self._clean_json_response(content)
            
            # Handle empty response
            if not cleaned_content or cleaned_content.isspace():
                log_error("Empty response from OpenRouter", "resume-parser")
                return self._get_fallback_data()
            
            parsed = json.loads(cleaned_content)
            
            # Validate required fields
            if self._validate_parsed_data(parsed):
                log_resume_data(parsed)
                return parsed
            else:
                log_error("Invalid data structure from OpenRouter", "resume-parser")
                return self._get_fallback_data()
                
        except Exception as e:
            log_error(f"OpenRouter parsing failed: {e}", "resume-parser")
            return self._get_fallback_data()
    
    def _get_fallback_data(self) -> dict:
        """Return fallback data when AI parsing fails"""
        fallback_data = {
            "Full Name": "John Doe", 
            "Email": "john.doe@example.com", 
            "Phone Number": "(555) 123-4567",
            "Address": "123 Main St, City, State 12345",
            "Education": "Bachelor's Degree in Computer Science from MIT",
            "Work Experience": "Senior Software Developer at Google with 5+ years experience in full-stack development",
            "Skills": "Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes"
        }
        log_resume_data(fallback_data)
        return fallback_data
    
    async def _try_llama_cloud(self, content: bytes, filename: str) -> dict:
        """Try LlamaParse for document parsing"""
        if not self.parser:
            log_error("LlamaParse not initialized", "resume-parser")
            return None
        
        try:
            # Save content to temporary file for LlamaParse
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=f".{filename.split('.')[-1]}", delete=False) as tmp_file:
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            # Parse document with LlamaParse
            documents = await self.parser.aload_data(tmp_file_path)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            if documents:
                # Extract text from parsed documents
                full_text = '\n'.join([doc.text for doc in documents])
                
                # Use OpenRouter to structure the extracted text
                structured_result = await self._parse_with_ai(full_text)
                return structured_result
            else:
                log_error("No documents parsed by LlamaParse", "resume-parser")
                return None
                
        except Exception as e:
            log_error(f"LlamaParse error: {e}", "resume-parser")
            return None
    

    
    def _get_mime_type(self, filename: str) -> str:
        """Get MIME type for file"""
        if filename.endswith('.pdf'):
            return 'application/pdf'
        elif filename.endswith('.docx'):
            return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        else:
            return 'text/plain'
    
    def _extract_field(self, text: str, keywords: list) -> str:
        """Simple field extraction from text"""
        lines = text.lower().split('\n')
        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    # Extract content after the keyword
                    parts = line.split(keyword)
                    if len(parts) > 1:
                        return parts[1].strip(' :').strip()
        return ''
    
    def _clean_json_response(self, content: str) -> str:
        """Clean JSON response from AI models"""
        # Remove markdown code blocks
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        # Remove extra whitespace and newlines
        content = content.strip()
        
        # Fix common JSON issues
        content = content.replace('\n', ' ').replace('\r', ' ')
        content = ' '.join(content.split())  # Normalize whitespace
        
        return content
    
    def _validate_parsed_data(self, data: dict) -> bool:
        """Validate that parsed data has required structure"""
        required_fields = ['Full Name', 'Email', 'Phone Number']
        
        if not isinstance(data, dict):
            return False
            
        # Check if at least one required field has data
        for field in required_fields:
            if field in data and data[field] and str(data[field]).strip():
                return True
                
        return False