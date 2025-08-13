from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from services.embedding_service import embed_pdf
from services.task_service import generate_task
import os


load_dotenv()

app = FastAPI()

INDEX_PATH = "data/faiss_index"
UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_PATH, exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    chunk_count = embed_pdf(file_path, INDEX_PATH)
    return {"message": f"{chunk_count}개의 청크가 임베딩되어 저장되었습니다."}

@app.get("/generate-task")
async def get_task(prompt: str):
    result = generate_task(prompt, INDEX_PATH)
    return {"task": result}
