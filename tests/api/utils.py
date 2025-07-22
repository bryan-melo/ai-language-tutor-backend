import pytest

from typing import Any
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError


def validate_and_create_instance(
   client: TestClient, 
   model_class: type[BaseModel],
   data: dict[str, Any], 
   status_code: int, 
   url: str
) -> dict[str, Any]:
   """
   Validate input with a Pydantic model and send POST request.

   Raises:
      - ValidationError: If the input data is invalid.

   Args:
      - client (TestClient): FastAPI test client.
      - model_class (type[BaseModel]): Model class for input validation.
      - data (dict[str, Any]): Payload to validate and send.
      - status_code (int): Expected HTTP response status code.
      - url (str): API endpoint URL.

   Returns:
      -  dict[str, Any]: Response JSON if created (201); otherwise, empty dict.
   """
   if status_code == status.HTTP_201_CREATED:
      validated = model_class.model_validate(data)
      assert isinstance(validated, model_class), f"Expected {model_class.__name__} instance, got {type(validated)}"
   else:
      with pytest.raises(ValidationError):
         model_class.model_validate(data)

   response = client.post(url, json=data)
   assert response.status_code == status_code, f"Expected {status_code}, got {response.status_code}"
   return response.json() if response.status_code == status.HTTP_201_CREATED else {}


def delete_instance(client: TestClient, instance_id: int, url: str) -> None:
   """
   Helper function to delete an account by ID.

   - Asserts 204 response on successful deletion
   - Asserts empty response body
   """
   response = client.delete(f"{url}{instance_id}")
   assert response.status_code == status.HTTP_204_NO_CONTENT, f"Expected 204, got {response.status_code}"
   assert response.text == "", "Expected empty response body on delete"
   