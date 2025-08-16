from dotenv import load_dotenv
import os

INDEX_PATH = "data/faiss_index"
UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_PATH, exist_ok=True)

load_dotenv()


