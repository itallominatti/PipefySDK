
from src.pipefysdk.errors.search_field_pipefy_error import SearchFieldPipefyError

class OrganizationService:
    def __init__(self, request_func, queries, mutations):
        self._request = request_func
        self._mutations = mutations
        self._queries = queries

    def get_users_from_organization(self, organization_id: int) -> list:
        query = self._queries.get_organization_users(organization_id)
        response = self._request(query)
        if 'errors' in response:
            raise PermissionError("Permission denied. you dont have access to this organization")
        return response.get("data", {}).get("organization", {}).get("users", [])

    def get_specific_user_from_organization(self, organization_id: int, email: str) -> dict:

        query = self._queries.get_organization_users(organization_id)
        response = self._request(query)
        try:
            users = response.get("data", {}).get("organization", {}).get("users", [])
        except:
            raise SearchFieldPipefyError("Email not found")

        for user in users:
            if user.get("email") == email:
                return user
        return None