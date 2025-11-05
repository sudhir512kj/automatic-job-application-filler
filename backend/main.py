from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from services.resume_parser import ResumeParser
from services.form_analyzer import FormAnalyzer
from services.form_filler import FormFiller
from services.google_forms_service import GoogleFormsService
from logger import log_request, log_response, log_error

load_dotenv()

app = FastAPI(title="Auto Form Filling Agent", version="1.0.0")

# Add environment-based CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if ALLOWED_ORIGINS == ["*"]:
    CORS_CREDENTIALS = False
else:
    CORS_CREDENTIALS = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class FormFillRequest(BaseModel):
    form_url: str

@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    log_request("/api/parse-resume", {"filename": file.filename, "size": file.size})
    
    try:
        if not file.filename.endswith(('.pdf', '.docx', '.txt')):
            log_error(f"Unsupported file format: {file.filename}", "parse-resume")
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        parser = ResumeParser()
        content = await file.read()
        extracted_data = await parser.extract_data(content, file.filename)
        
        response = {"status": "success", "data": extracted_data}
        log_response("/api/parse-resume", response)
        return response
    except Exception as e:
        log_error(str(e), "parse-resume")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-form")
async def analyze_form(request: FormFillRequest):
    log_request("/api/analyze-form", {"form_url": request.form_url})
    
    try:
        # Use Google Forms service instead of Selenium
        google_forms = GoogleFormsService()
        form_structure = await google_forms.get_form_structure(request.form_url)
        
        response = {"status": "success", "fields": form_structure["fields"], "form_id": form_structure["form_id"]}
        log_response("/api/analyze-form", response)
        return response
    except Exception as e:
        log_error(str(e), "analyze-form")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fill-form")
async def fill_form(
    form_url: str = Form(...),
    file: UploadFile = File(...)
):
    log_request("/api/fill-form", {"form_url": form_url, "filename": file.filename})
    
    try:
        parser = ResumeParser()
        google_forms = GoogleFormsService()
        
        # Parse resume
        content = await file.read()
        resume_data = await parser.extract_data(content, file.filename)
        
        # Submit form directly using Google Forms API
        result = await google_forms.submit_form_response(form_url, resume_data)
        
        log_response("/api/fill-form", result)
        return result
    except Exception as e:
        log_error(str(e), "fill-form")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hello")
async def hello_world():
    return {"message": "Hello World!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)