import pytest
from pydantic import ValidationError
from app.models.chat_models import ChatRequest


class TestChatModels:
   # Test ChatRequest model for valid instance
   def test_chat_request_model_valid(self):
      data = {
         "user_input": "Hello World!",
         "prompt_text": "Testing chat request model",
         "role_prompt": "Be nice."
      }
      chat_request = ChatRequest(**data)
      
      assert chat_request.user_input == "Hello World!"
      assert chat_request.prompt_text == "Testing chat request model"
      assert chat_request.role_prompt == "Be nice."
      
      
   # Test ChatRequest model for invalid instance --invalid type
   def test_chat_request_model_invalid_type(self):
      with pytest.raises(ValidationError):
         ChatRequest.model_validate({
            "user_input": "Hello World!",
            "prompt_text": "Testing chat request model",
            "role_prompt": 1234
         })
