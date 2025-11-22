from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import time
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

# Add CORS configuration for Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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

import asyncio
from concurrent.futures import ThreadPoolExecutor

# Global task storage
processing_tasks = {}

@app.post("/api/fill-form")
async def fill_form(
    form_url: str = Form(...),
    file: UploadFile = File(...)
):
    task_id = f"task_{int(time.time() * 1000)}"
    log_request("/api/fill-form", {"task_id": task_id, "form_url": form_url, "filename": file.filename})
    
    try:
        content = await file.read()
        
        # Start async processing
        processing_tasks[task_id] = {"status": "processing", "progress": 0}
        asyncio.create_task(process_form_async(task_id, form_url, content, file.filename))
        
        return {"task_id": task_id, "status": "started", "message": "Processing started"}
    except Exception as e:
        log_error(str(e), "fill-form")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/task-status/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in processing_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return processing_tasks[task_id]

async def process_form_async(task_id: str, form_url: str, content: bytes, filename: str):
    try:
        processing_tasks[task_id] = {"status": "processing", "progress": 10, "message": "Parsing resume..."}
        
        # Parse resume in thread pool
        parser = ResumeParser()
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            resume_data = await loop.run_in_executor(executor, 
                lambda: asyncio.run(parser.extract_data(content, filename)))
        
        processing_tasks[task_id] = {"status": "processing", "progress": 60, "message": "Analyzing form..."}
        
        # Submit form
        google_forms = GoogleFormsService()
        result = await google_forms.submit_form_response(form_url, resume_data)
        
        processing_tasks[task_id] = {"status": "completed", "progress": 100, "result": result}
        
    except Exception as e:
        processing_tasks[task_id] = {"status": "error", "error": str(e)}

@app.get("/api/hello")
async def hello_world():
    return {"message": "Hello World!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)