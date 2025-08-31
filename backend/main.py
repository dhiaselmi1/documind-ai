
# ===============================
# backend/main.py
# ===============================

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
import docx
import io
import uuid
from typing import Dict, List, Optional
from agents.orchestrator import AgentOrchestrator

app = FastAPI(title="Document Intelligence API", version="1.0.0")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
documents: Dict[str, dict] = {}
analysis_results: Dict[str, dict] = {}

# Initialize orchestrator
orchestrator = AgentOrchestrator()


class AnalysisResponse(BaseModel):
    document_id: str
    filename: str
    summary: str
    red_flags: List[str]
    decisions: List[str]
    status: str


class DocumentInfo(BaseModel):
    id: str
    filename: str
    content: str
    file_type: str


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file."""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading DOCX: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file."""
    try:
        return file_content.decode('utf-8').strip()
    except UnicodeDecodeError:
        try:
            return file_content.decode('latin-1').strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading TXT: {str(e)}")


@app.post("/upload", response_model=DocumentInfo)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document."""

    # Validate file type
    allowed_types = ['.pdf', '.docx', '.txt']
    file_extension = '.' + file.filename.split('.')[-1].lower()

    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_extension} not supported. Allowed: {allowed_types}"
        )

    # Read file content
    file_content = await file.read()

    # Extract text based on file type
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_content)
    elif file_extension == '.docx':
        text = extract_text_from_docx(file_content)
    elif file_extension == '.txt':
        text = extract_text_from_txt(file_content)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the file")

    # Store document
    doc_id = str(uuid.uuid4())
    documents[doc_id] = {
        "id": doc_id,
        "filename": file.filename,
        "content": text,
        "file_type": file_extension
    }

    return DocumentInfo(**documents[doc_id])


@app.post("/analyze/{document_id}", response_model=AnalysisResponse)
async def analyze_document(document_id: str):
    """Analyze a document with all agents."""
    print("1")

    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")


    document = documents[document_id]

    try:
        # Run analysis through orchestrator
        print("2")
        results = await orchestrator.analyze_document(document["content"])
        print("3")

        # Store results
        analysis_results[document_id] = results

        return AnalysisResponse(
            document_id=document_id,
            filename=document["filename"],
            summary=results["summary"],
            red_flags=results["red_flags"],
            decisions=results["decisions"],
            status="completed"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/documents")
async def get_documents():
    """Get all uploaded documents."""
    return list(documents.values())


@app.get("/analysis/{document_id}")
async def get_analysis(document_id: str):
    """Get analysis results for a document."""
    if document_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return analysis_results[document_id]


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agents": orchestrator.get_agent_status()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)







