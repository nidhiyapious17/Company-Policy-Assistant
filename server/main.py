from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "Company Policy assistant app loading"}

@app.post('/api/chat')
def ask_question(request):
    query = request.query
    print(query)

 