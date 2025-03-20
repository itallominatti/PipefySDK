from typing import Optional
import base64
import binascii

import httpx

from src.pipefysdk.base_service import BaseService
from src.pipefysdk.queries.query_cards import GraphQLQueries
from src.pipefysdk.utils.binary_tree import BinarySearchTree
from src.pipefysdk.errors.card_move_pipefy_error import CardMovePipefyError
from src.pipefysdk.errors.search_field_pipefy_error import SearchFieldPipefyError
from src.pipefysdk.errors.permission_error import PermissionError


class PipefySDK(BaseService):
    def __init__(self, token: str, url: str) -> None:
        super().__init__(pipefy_token=token, url=url)
        self.queries = GraphQLQueries()

    def get_card_info(self, card_id: int) -> dict:
        """
        Get card information by card id.

        args:
            card_id: Define the card id to get the information.

        return: Return the card information.
        """
        query = self.queries.search_fields_in_card(card_id=card_id)
        response = self.request(query)
        return response.get("data").get("card")

    def update_single_card_field(self, card_id: str, field_id: str, new_value: str) -> dict:
        """
        Update a single card field.

        args:
            card_id: Define the card id to update the field.
            field_id: Define the field id to update.
            new_value: Define the new value to be updated.

        return: Return the response of the API.
        """
        mutation = self.mutations.mutation_update_card_field(card_id, field_id, new_value)
        return self.request(mutation).get("data", {}).get("updateFieldsValues", {})

    def update_multiple_card_fields(self, card_id: str, fields: list) -> dict:
        """
        Update multiple card fields.

        args:
            card_id: Define the card id to update the fields.
            fields: Define the fields to be updated.

        return: Return the response of the API.
        """
        mutation = self.mutations.mutation_update_card_field(card_id, fields=fields)
        return self.request(mutation).get("data", {}).get("updateFieldsValues", {})

    def search_value_in_field(self, card_id: int, field_id: str) -> Optional[str]:
        """
        Search a value in a card field.

        args:
            card_id: Define the card id to search for the value.
            field_id: Define the field id to search for the value.

        return: Return the value of the field or None if not found.
        """
        query = self.queries.search_fields_in_card(card_id)
        response = self.request(query)
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
        """
        Search multiple values in card fields.

        args:
            card_id: Define the card id to search for the values.
            field_ids: Define the fields ids to search for the values.

        return: Return the values of the fields.
        """
        query = self.queries.search_fields_in_card(card_id)
        response = self.request(query)
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

    def move_card_to_phase(self, new_phase_id: int, card_id: int) -> dict:
        """
            Move a card to a new phase.

            Args:
                new_phase_id (int): The ID of the new phase.
                card_id (int): The ID of the card to move.

            Returns:
                dict: The response from the API.
        """
        mutation = self.mutations.mutation_move_card_to_phase(card_id=card_id, phase_id=new_phase_id)
        response = self.request(mutation)
        if 'errors' in response:
            raise CardMovePipefyError(f"{response['errors']}. Probably, you have required fields empty in your card.")
        return response

    def get_attachments_from_card(self, card_id: int) -> list:
        """
        Get attachments from a card.

        Args:
            card_id (int): The ID of the card.

        Returns:
            list: The response from the API.
        """
        query = self.queries.get_attachments_from_card(card_id)
        response = self.request(query)
        return response.get("data", {}).get("card", {}).get("attachments", [])

    def set_assignee_in_card(self, card_id: int, assignee_ids: list) -> dict:
        """
        Search users in a pipe.

        Args:
            card_id (int): The ID of the card.
            assignee_ids (list): The list of assignee IDs.

        Returns:
            dict: The response from the API.
        """
        query = self.mutations.update_card_assignee(card_id, assignee_ids)
        response = self.request(query)
        return response.get("data", {}).get("pipe", {}).get("users", {})

    def upload_and_attach_file(self, card_id: int, field_id: str, file_base64: str, file_name: str,
                               organization_id: int) -> dict:
        """
        Upload a base64 file and attach it to a card.

        Args:
            card_id (int): The ID of the card.
            field_id (str): The ID of the field to attach the file to.
            file_base64 (str): The base64 encoded file content.
            file_name (str): The name of the file.
            organization_id (int): The ID of the organization.

        Returns:
            dict: The response from the API.
        """
        # Check if the file_base64 is valid
        try:
            file_bytes = base64.b64decode(file_base64)
        except binascii.Error:
            raise ValueError("Invalid base64 file content")

        # Step 1: Generate pre-signed URL
        mutation = self.mutations.mutation_create_pre_assigned_url(organization_id, file_name)
        response = self.request(mutation)

        if 'errors' in response:
            raise PermissionError("You need to be on the enterprise plan to use this feature")

        presigned_url = response['data']['createPresignedUrl']['url']

        upload_response = httpx.put(presigned_url, content=file_bytes, headers={'Content-Type': 'application/pdf'})
        upload_response.raise_for_status()

        path_to_send = presigned_url.split('.com/')[1].split('?')[0]

        mutation = self.mutations.mutation_update_card_field(card_id, field_id, path_to_send)
        attach_response = self.request(mutation)
        return attach_response

    def send_email(self, card_id: int, repo_id: int, from_email: str, subject: str, text: str, to_email: str) -> dict:
        mutation_create_email = self.mutations.mutation_create_inbox_email(card_id, repo_id, from_email, subject, text,
                                                                           to_email)
        response_create_email = self.request(mutation_create_email)

        if 'errors' in response_create_email:
            raise RuntimeError(f"Failed to create inbox email: {response_create_email['errors']}")

        email_id = response_create_email['data']['createInboxEmail']['inbox_email']['id']
        mutation_send_email = self.mutations.mutation_send_inbox_email(email_id)
        response_send_email = self.request(mutation_send_email)

        return response_send_email




