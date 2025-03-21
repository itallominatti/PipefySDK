from typing import List, Optional

from src.pipefysdk.models.models import FieldAttribute

from src.pipefysdk.errors.card_create_pipefy_error import CardCreatePipefyError
from src.pipefysdk.errors.search_field_pipefy_error import SearchFieldPipefyError

from src.pipefysdk.utils.binary_tree import BinarySearchTree

class CardService:
    def __init__(self, request_func, queries, mutations):
        self._request = request_func
        self._mutations = mutations
        self._queries = queries

    def create_card(self, pipe_id: int, fields: List[FieldAttribute]) -> dict:
        mutation = self._mutations.mutation_create_card(pipe_id, fields)
        response = self._request(mutation)
        if 'errors' in response:
            raise CardCreatePipefyError(f"Failed to create card: {response['errors']}")
        return response

    def delete_card(self, card_id: int) -> dict:
        mutation = self._mutations.mutation_delete_card(card_id)
        response = self._request(mutation)
        return response

    def get_card_info(self, card_id: int) -> dict:
        query = self._queries.search_fields_in_card(card_id=card_id)
        response = self._request(query)
        return response.get("data").get("card")

    def update_single_card_field(self, card_id: str, field_id: str, new_value: str) -> dict:
        mutation = self._mutations.mutation_update_card_field(card_id, field_id, new_value)
        return self._request(mutation).get("data", {}).get("updateFieldsValues", {})

    def update_multiple_card_fields(self, card_id: str, fields: list) -> dict:
        mutation = self._mutations.mutation_update_card_field(card_id, fields=fields)
        return self._request(mutation).get("data", {}).get("updateFieldsValues", {})

    def search_value_in_field(self, card_id: int, field_id: str) -> Optional[str]:
        query = self._queries.search_fields_in_card(card_id)
        response = self._request(query)
        try:
            fields = response.get("data", {}).get("card", {}).get("fields", [])
        except:
            raise SearchFieldPipefyError("Field not found")
        bst = BinarySearchTree()
        for field in fields:
            field_key = field.get("field", {}).get("id")
            field_value = field.get("value")
            bst.insert(field_key, field_value)

        result_node = bst.search(field_id)
        return result_node.value if result_node else None

    def search_multiple_values_in_fields(self, card_id: int, field_ids: list) -> dict:
        query = self._queries.search_fields_in_card(card_id)
        response = self._request(query)
        try:
            fields = response.get("data", {}).get("card", {}).get("fields", [])
        except:
            raise SearchFieldPipefyError("Field not found")

        bst = BinarySearchTree()
        for field in fields:
            field_key = field.get("field", {}).get("id")
            field_value = field.get("value")
            bst.insert(field_key, field_value)

        result = {}
        for field_id in field_ids:
            result_node = bst.search(field_id)
            result[field_id] = result_node.value if result_node else None
        return result

    def get_attachments_from_card(self, card_id: int) -> list:
        query = self._queries.get_attachments_from_card(card_id)
        response = self._request(query)
        return response.get("data", {}).get("card", {}).get("attachments", [])

    def set_assignee_in_card(self, card_id: int, assignee_ids: list) -> dict:
        query = self._mutations.update_card_assignee(card_id, assignee_ids)
        response = self._request(query)
        return response.get("data", {}).get("pipe", {}).get("users", {})