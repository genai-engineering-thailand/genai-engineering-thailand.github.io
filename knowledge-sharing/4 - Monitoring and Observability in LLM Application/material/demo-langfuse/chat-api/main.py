from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.custom_exception import handle_errors
from src.llm import conversation
from src.request_model import Chat

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"success": True}

@app.post("/chat/message")
@handle_errors
def chat(data: Chat):
    answer, trace_id= conversation(data.name, data.session_id, data.message)

    return {
        "success": True,
        "data": {
            "answer": answer,
            "trace_id": trace_id
        },
    }