from fastapi import FastAPI, File, UploadFile
from model.model import ChatRequest
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.get('/')
def read_root():
    return {"message": "Company Policy assistant app loading"}

@app.post('/api/chat')
def ask_question(request: ChatRequest):
    query = request.query

@app.post('/api/upload_docs')
async def upload_docs(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
    }

 
