from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str  # "user" o "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    extracted_entities: List[str] = []
    conversation_id: str

class Conversation(BaseModel):
    id: str
    messages: List[Message] = []