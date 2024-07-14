from pydantic import BaseModel

class Chat(BaseModel):
    name: str
    session_id: str
    message_id: str
    message: str