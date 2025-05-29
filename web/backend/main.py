import sys
import os
# Add the project root to Python path so we can import from src/
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tempfile
import shutil
from src.utils.file_handler import is_valid_pdf, get_file_info
from src.pdf_merger import PdfMerger

app = FastAPI(title="PDF Merger API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "PDF Merger API is running"}

@app.post("/validate-files")
async def validate_files(files: List[UploadFile] = File(...)):
    """Validate uploaded PDF files without processing them"""
    results = []
    
    for file in files:
        # Save file temporarily for validation
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Validate using your existing function
            is_valid = is_valid_pdf(temp_file.name)
            file_info = get_file_info(temp_file.name) if is_valid else None
            
            results.append({
                "filename": file.filename,
                "is_valid": is_valid,
                "size": len(content),
                "size_kb": round(len(content) / 1024, 1),
                "error": None if is_valid else "Invalid PDF file"
            })
            
            # Cleanup temp file
            os.unlink(temp_file.name)
    
    return {"files": results}

@app.post("/merge-pdfs")
async def merge_pdfs(files: List[UploadFile] = File(...)):
    """Merge multiple PDF files into one using your existing PdfMerger"""
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least 2 PDF files required")
    
    temp_files = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save uploaded files temporarily
        for i, file in enumerate(files):
            content = await file.read()
            temp_file_path = os.path.join(temp_dir, f"input_{i}.pdf")
            
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(content)
            
            # Validate each file using your existing function
            if not is_valid_pdf(temp_file_path):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid PDF file: {file.filename}"
                )
            
            temp_files.append(temp_file_path)
        
        # Create output file
        output_path = os.path.join(temp_dir, "merged_output.pdf")
        
        # Use your existing PdfMerger class
        merger = PdfMerger()
        success = merger.merge_pdfs(temp_files, output_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="PDF merge failed")
        
        # Return the merged file
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename="merged.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Merge failed: {str(e)}")
    
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}