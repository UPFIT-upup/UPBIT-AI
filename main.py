from fastapi import FastAPI
from app.routes import router

app = FastAPI()
app.include_router(router)

#uvicorn main:app --reload : 실행 명령어