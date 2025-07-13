import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_get_all_accounts():
   async with AsyncClient(app=app, base_url="http://test") as client:
      response = await client.get("/account/get-all-accounts")
      
      # Verify status code
      assert response.status_code == 200
      