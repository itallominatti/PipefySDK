import asyncio
import logging
import httpx
from pydantic import ValidationError
from src.pipefysdk.models.request_model import RequestModel
from src.pipefysdk.errors.http_request_pipefy_error import HttpRequestPipefyError

class HttpClient:
    def __init__(self, url: str, headers: dict, timeout_connection: int = 10, max_attempts: int = 5, retry_delay: int = 2) -> None:
        self.url = url
        self.headers = headers
        self.timeout_connection = timeout_connection
        self.max_attempts = max_attempts
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)

    async def post(self, query: str) -> dict:
        try:
            request_data = RequestModel(query=query)
        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            raise

        attempt = 0
        while attempt < self.max_attempts:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self.url,
                        headers=self.headers,
                        json=request_data.model_dump_json(),
                        timeout=self.timeout_connection
                    )
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPStatusError as e:
                self.logger.error(f"HTTP error occurred: {e}")
                if e.response.status_code == 429:
                    self.logger.info(f"Throttling detected. Retrying in {self.retry_delay} seconds...")
                    await asyncio.sleep(self.retry_delay)
                    attempt += 1
                else:
                    raise
            except httpx.RequestError as e:
                self.logger.error(f"Request error occurred: {e}")
                await asyncio.sleep(self.retry_delay)
                attempt += 1
        raise HttpRequestPipefyError(
            message="Max attempts reached. For more information, visit: https://developers.pipefy.com/reference/status-and-error-handling",
            status_code=500
        )