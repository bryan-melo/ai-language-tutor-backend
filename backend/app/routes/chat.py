from fastapi import APIRouter, HTTPException
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import os
from app.models.chat_models import ChatRequest

load_dotenv()
router = APIRouter()

# Set the API key
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create clients using the new SDK format
client = OpenAI(api_key=OPEN_AI_API_KEY)
async_client = AsyncOpenAI(api_key=OPEN_AI_API_KEY)

@router.post("/chat")
async def chat_with_gpt(request: ChatRequest):
    try:
        system_prompt = request.role_prompt or (
            "You are a helpful language tutor. The user practices pronunciation and spelling by typing words or sentences. "
            "Provide text-based feedback, corrections, and explanations. "
            "Do NOT mention you can't hear or evaluate pronunciation."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.user_input},
        ]

        response = await async_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))