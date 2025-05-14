import os
from dotenv import load_dotenv
import openai
from fastapi import APIRouter, HTTPException
from app.models.chat_models import ChatRequest

router = APIRouter()

# Load the .env file
load_dotenv()

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")


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
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))