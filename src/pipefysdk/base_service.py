from src.pipefysdk.queries.query_cards import GraphQLQueries

import httpx

class BaseService:
    """
    Base class for all services.

    url: Define the bas url with the endpoint "/graphql".
    pipefy_token: Define the token to access the API without the name "Bearer".
    """
    def __init__(self, url: str, pipefy_token: str) -> None:
        self.url = url
        self._pipefy_token = pipefy_token
        self.headers = {
            'Authorization': f'Bearer {self._pipefy_token}',
            'Content-Type': 'application/json'
        }
        self.timeout_connection = 10
        self.attemps_connection = 10
        self.queries = GraphQLQueries()

    async def request(self, query: str) -> dict:
        """
        Make a request to the API.

        query: Define the query to be sent to the API.

        return: Return the response of the API.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                headers=self.headers,
                json={'query': query},
                timeout=self.timeout_connection,
                retries=self.attemps_connection
            )
            return response.json()