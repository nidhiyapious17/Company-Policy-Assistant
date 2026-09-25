from fastapi import FastAPI, File, UploadFile, HTTPException
from model.model import ChatRequest
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

app = FastAPI()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

base_dir = Path(__file__).resolve().parent

chroma_dir = base_dir/ 'chroma_db'

#This creates a Path object pointing to folder uploads
upload_dir = base_dir/'uploads'

#This creates a folder if it does not exists
upload_dir.mkdir(exist_ok=True)

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

#Save the file uploaded
@app.post('/api/upload_docs')
async def upload_docs(file: UploadFile = File(...)):
    contents = await file.read() #It will return contents in bytes

    if not contents:
        raise HTTPException(
            status_code=400,
            detail = 'The uploaded file is empty'
        )
    #craete a unique id and server side file name
    document_id = str(uuid4())
    saved_file_path = upload_dir/f"{document_id}.pdf"

    #Save the pdf locally
    saved_file_path.write_bytes(contents)

    loader = PyPDFLoader(str(saved_file_path))
    pages = loader.load()

    print(f"Total pages extracted : {len(pages)}")
    print(pages[0].page_content[:300])

    #Split the pdf pages into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 5
    )

    chunks = text_splitter.split_documents(pages)

    print(f"\n\nTotal chunks created\n\n: {len(chunks)}")
    print("---First chunk-----")
    print(chunks[0].page_content)
    print("---Chunk meta data ----")
    print(chunks[0].metadata)

    #Add metadata and stable ids to each chunk
    for index, chunk in enumerate(chunks):
        chunk.metadata.update({
            "document_id": document_id,
            "file_name": file.filename,
            "chunk_index": index
        })

    chunk_ids = [
        f"{document_id}_chunk_{index}"
        for index in range(len(chunks))
    ]

    print("------chunk metadata------")

    print(chunks[0].metadata)
    print(chunk_ids[0])

    #create embeddings and store the chunks in vector store
    vector_store = Chroma(
        collection_name="pdf_uploader",
        embedding_function=embeddings,
        persist_directory=str(chroma_dir)
    )

    vector_store.add_documents(documents=chunks, ids=chunk_ids)

    print(f"Stored {len(chunks)} chunks in Chroma.")



    return {
        "document_id": document_id,
        "file_name": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "status": "uploaded"
    }
    

 
