from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.embedding_service import embed_file
from services.task_service import generate_task
from app.config import UPLOAD_DIR, INDEX_PATH
import os

router = APIRouter()
ALLOWED_EXTENSIONS = {".pdf", ".txt",".html", ".json", ".docx", ".xlsx", ".pptx"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. PDF, TXT, HTML, JSON, DOCX, XLSX, PPTX만 업로드 가능합니다."
        )
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # TODO: 확장자별 다른 임베딩 함수로 변경 가능
    chunk_count = embed_file(file_path, INDEX_PATH)
    
    return {"message": f"{chunk_count}개의 청크가 임베딩되어 저장되었습니다."}

@router.get("/generate-task")
async def get_task(prompt: str):
    result = generate_task(prompt, INDEX_PATH)
    return {"task": result}
