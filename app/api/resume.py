from fastapi import APIRouter, UploadFile, File, HTTPException
import PyPDF2

router = APIRouter()

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        return {
            "resume_text": text[:1000],   # small preview
            "ranked_jobs": ["Software Engineer", "Data Scientist", "ML Engineer"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
