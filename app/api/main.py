from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import fitz  # PyMuPDF
import os
from app.api.agent import run_agent

app = FastAPI()


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text safely from a PDF given as bytes."""
    try:
        # Write bytes to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name

        # Open and read with PyMuPDF
        doc = fitz.open(tmp_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        doc.close()

        # Clean up temp file
        os.remove(tmp_path)

        return text
    except Exception as e:
        # Optional: log e
        return ""
    

@app.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Basic validation
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        pdf_bytes = await file.read()
        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        # Extract text
        text = extract_text_from_pdf(pdf_bytes)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

        # Build query for the agent
        query = f"Match this resume to jobs and rank them:\n{text}"

        # Call your agent
        result = run_agent(query)

        # Normalize result so it is JSON-serializable
        if isinstance(result, (bytes, bytearray)):
            result = result.decode("utf-8", errors="ignore")
        elif not isinstance(result, (list, dict, str)):
            result = str(result)

        return JSONResponse(
            content={
                "resume_text": text[:500],  # preview
                "ranked_jobs": result
            },
            status_code=200
        )

    except HTTPException:
        # Re-raise HTTPExceptions as they already have status codes
        raise
    except Exception as e:
        # Log the error here if you have logging configured
        return JSONResponse(
            content={"error": f"Backend crash in /resume: {repr(e)}"},
            status_code=500
        )


@app.get("/")
def root():
    return {"status": "OK"}
