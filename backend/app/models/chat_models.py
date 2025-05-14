from pydantic import BaseModel

# Request schema
class ChatRequest(BaseModel):
    user_input: str
    prompt_text: str