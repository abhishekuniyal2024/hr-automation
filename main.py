from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import json
import os
import uuid
import PyPDF2
import docx
from typing import Dict, List, Optional

from recruitment_orchestrator_langgraph import LangGraphRecruitmentOrchestrator
from config import APP_NAME, APP_VERSION

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-Powered Recruitment System with Multi-Agent Coordination using LangGraph"
)

# Initialize recruitment orchestrator with LangGraph
orchestrator = LangGraphRecruitmentOrchestrator()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create necessary directories
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with recruitment dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/start-recruitment")
async def start_recruitment():
    """Start the recruitment process by analyzing employee data"""
    try:
        result = orchestrator.start_recruitment_process()
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/job-openings")
async def get_job_openings():
    """Get all current job openings"""
    try:
        return JSONResponse(content={
            "status": "success",
            "job_openings": orchestrator.state.get("job_openings", [])
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/apply")
async def apply_for_job(
    candidate_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    position: str = Form(...),
    experience_years: str = Form(...),  # Changed from int to str
    resume_text: str = Form(...)
):
    """Process a candidate application"""
    try:
        # Convert experience_years to int with error handling
        try:
            experience_years_int = int(experience_years)
        except ValueError:
            raise HTTPException(status_code=422, detail="Experience years must be a valid number")
        
        candidate_data = {
            "candidate_id": f"candidate_{len(orchestrator.state.get('candidates', [])) + 1}",
            "candidate_name": candidate_name,
            "email": email,
            "phone": phone,
            "position": position,
            "experience_years": experience_years_int,
            "resume_text": resume_text,
            "cover_letter": "Not provided"  # Default value since field was removed
        }
        
        result = orchestrator.process_candidate_application(candidate_data, position)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/candidates")
async def get_candidates():
    """Get all candidates"""
    try:
        return JSONResponse(content={
            "status": "success",
            "candidates": orchestrator.state.get("candidates", [])
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview/{candidate_id}/{stage}")
async def conduct_interview(
    candidate_id: str,
    stage: str,
    feedback: str = Form("")
):
    """Conduct an interview stage"""
    try:
        result = orchestrator.conduct_interview(candidate_id, stage, feedback)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/select/{candidate_id}")
async def make_selection(
    candidate_id: str,
    decision: str = Form(...),
    notes: str = Form("")
):
    """Make final selection decision"""
    try:
        result = orchestrator.make_final_selection(candidate_id, decision, notes)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/summary")
async def get_recruitment_summary():
    """Get recruitment process summary"""
    try:
        summary = orchestrator.generate_recruitment_summary()
        return JSONResponse(content=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_system_status():
    """Get system status and health"""
    try:
        return JSONResponse(content={
            "status": "healthy",
            "app_name": APP_NAME,
            "version": APP_VERSION,
            "job_openings_count": len(orchestrator.state.get("job_openings", [])),
            "candidates_count": len(orchestrator.state.get("candidates", [])),
            "interviews_count": len([c for c in orchestrator.state.get("candidates", []) if c.get("status") == "interview_scheduled"]),
            "hired_count": len([c for c in orchestrator.state.get("candidates", []) if c.get("status") == "hired"])
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_text_from_file(file: UploadFile) -> str:
    """Extract text content from uploaded file"""
    try:
        content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        if file.filename.lower().endswith('.pdf'):
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(file.file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif file.filename.lower().endswith(('.doc', '.docx')):
            # Extract text from Word document
            doc = docx.Document(file.file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file.filename.lower().endswith('.txt'):
            # Read text file
            return content.decode('utf-8')
        
        else:
            raise ValueError(f"Unsupported file type: {file.filename}")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file {file.filename}: {str(e)}")

@app.post("/api/upload-resumes")
async def upload_resumes(resumes: List[UploadFile] = File(...)):
    """Upload and analyze multiple resumes using AI"""
    try:
        if not resumes:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        if len(resumes) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 resumes allowed")
        
        candidates = []
        
        for file in resumes:
            try:
                # Extract text from file
                resume_text = extract_text_from_file(file)
                
                # Generate candidate name from filename
                candidate_name = os.path.splitext(file.filename)[0].replace('_', ' ').title()
                
                # Create candidate data
                candidate_data = {
                    "candidate_id": f"candidate_{uuid.uuid4().hex[:8]}",
                    "candidate_name": candidate_name,
                    "filename": file.filename,
                    "resume_text": resume_text,
                    "email": f"{candidate_name.lower().replace(' ', '.')}@example.com",
                    "phone": "Not provided",
                    "position": "Senior Software Engineer",  # Default position
                    "experience_years": 3,  # Default experience
                    "cover_letter": "Not provided"
                }
                
                # Use AI to score the candidate
                scoring_result = orchestrator.score_candidate_resume(candidate_data)
                
                # Combine candidate data with scoring results
                candidate_result = {
                    **candidate_data,
                    **scoring_result
                }
                
                candidates.append(candidate_result)
                
            except Exception as e:
                # Skip problematic files but continue with others
                print(f"Error processing {file.filename}: {str(e)}")
                continue
        
        if not candidates:
            raise HTTPException(status_code=400, detail="No valid resumes could be processed")
        
        return JSONResponse(content={
            "status": "success",
            "message": f"Successfully analyzed {len(candidates)} resumes",
            "candidates": candidates
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/hire-candidate")
async def hire_candidate(request: Request):
    """Hire the selected candidate"""
    try:
        data = await request.json()
        candidate_id = data.get("candidate_id")
        decision = data.get("decision", "hired")
        notes = data.get("notes", "")
        
        if not candidate_id:
            raise HTTPException(status_code=400, detail="Candidate ID is required")
        
        # Add candidate to orchestrator
        result = orchestrator.add_candidate_from_scoring(candidate_id, decision, notes)
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
