from fastapi import APIRouter, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.chat_models import ChatRequest

load_dotenv()
router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/chat")
async def chat_with_gpt(request: ChatRequest):
    try:
        messages = [
            {
                "role": "system",
                "content": f"You're a pronunciation tutor. Evaluate how the user pronounces: \"{request.prompt_text}\".",
            },
            {"role": "user", "content": request.user_input},
        ]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))