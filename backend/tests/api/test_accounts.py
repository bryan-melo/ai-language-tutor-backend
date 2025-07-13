import pytest
from httpx import AsyncClient
from main import app




'''
   Considerations:
      - Think like an external client calling this API (black-box testing).
      - Cover both positive (happy paths) and negative (error paths) scenarios.
      - Clear structure (pytest functions and fixtures), easy maintenance, and possible CI integrations (GitHub Actions).
      
   Approach:
      - Use httpx for HTTP-level tests to test async and more real-world behavior.
      - 
'''
 
