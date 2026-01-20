from fastapi import HTTPException
from typing import Any, Dict
import requests

class LLMService:
    def __init__(self, llm_api_url: str):
        self.llm_api_url = llm_api_url

    def generate_response(self, user_query: str) -> Dict[str, Any]:
        try:
            response = requests.post(self.llm_api_url, json={"query": user_query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(err)}")