from typing import Optional

from pipefysdk.base_service import BaseService
from pipefysdk.utils.constraints import DEFAULT_BASE64, DEFAULT_NAME
from pipefysdk.models.models import FieldAttribute
from pipefysdk.services.card_service import CardService
from pipefysdk.services.phase_service import PhaseService
from pipefysdk.services.report_service import ReportService
from pipefysdk.services.attachment_service import AttachmentService
from pipefysdk.services.email_service import EmailService
from pipefysdk.services.organization_service import OrganizationService


class PipefySDK(BaseService):
    def __init__(self, token: str, url: str) -> None:
        super().__init__(pipefy_token=token, url=url)
        self.card_service = CardService(self.request,self.queries,self.mutations)
        self.phase_service = PhaseService(self.request,self.queries,self.mutations)
        self.report_service = ReportService(self.request,self.queries,self.mutations)
        self.attachment_service = AttachmentService(self.request,self.queries,self.mutations)
        self.email_service = EmailService(self.request,self.queries,self.mutations)
        self.organization_service = OrganizationService(self.request,self.queries,self.mutations)

    def request(self, query: str) -> dict:
        """
        Make a request to the API.

        query: Define the query to be sent to the API. Example: query = "{ allPipes { id name } }"

        return: Return the response of the API.
        """
        return self.http_client.post(query)

    def get_card_info(self, card_id: int) -> dict:
        """
        Get card information by card id.

        args:
            card_id: Define the card id to get the information.

        return: Return the card information.
        """
        return self.card_service.get_card_info(card_id)

    def update_single_card_field(self, card_id: str, field_id: str, new_value: str) -> dict:
        """
        Update a single card field.

        args:
            card_id: Define the card id to update the field.
            field_id: Define the field id to update.
            new_value: Define the new value to be updated.

        return: Return the response of the API.
        """
        return self.card_service.update_single_card_field(card_id, field_id, new_value)

    def update_multiple_card_fields(self, card_id: str, fields: list) -> dict:
        """
        Update multiple card fields.

        args:
            card_id: Define the card id to update the fields.
            fields: Define the fields to be updated.

        return: Return the response of the API.
        """
        return self.card_service.update_multiple_card_fields(card_id, fields)

    def search_value_in_field(self, card_id: int, field_id: str) -> Optional[str]:
        """
        Search a value in a card field.

        args:
            card_id: Define the card id to search for the value.
            field_id: Define the field id to search for the value.

        return: Return the value of the field or None if not found.
        """
        return self.card_service.search_value_in_field(card_id, field_id)

    def search_multiple_values_in_fields(self, card_id: int, field_ids: list) -> dict:
        """
        Search multiple values in card fields.

        args:
            card_id: Define the card id to search for the values.
            field_ids: Define the fields ids to search for the values.

        return: Return the values of the fields.
        """
        return self.card_service.search_multiple_values_in_fields(card_id, field_ids)

    def move_card_to_phase(self, new_phase_id: int, card_id: int) -> dict:
        """
            Move a card to a new phase.

            Args:
                new_phase_id (int): The ID of the new phase.
                card_id (int): The ID of the card to move.

            Returns:
                dict: The response from the API.
        """
        return self.phase_service.move_card_to_phase(new_phase_id, card_id)

    def get_attachments_from_card(self, card_id: int) -> list:
        """
        Get attachments from a card.

        Args:
            card_id (int): The ID of the card.

        Returns:
            list: The response from the API.
        """
        return self.card_service.get_attachments_from_card(card_id)

    def set_assignee_in_card(self, card_id: int, assignee_ids: list) -> dict:
        """
        Search users in a pipe.

        Args:
            card_id (int): The ID of the card.
            assignee_ids (list): The list of assignee IDs.

        Returns:
            dict: The response from the API.
        """
        return self.card_service.set_assignee_in_card(card_id, assignee_ids)

    def upload_and_attach_file(self, card_id: int, organization_id: int, field_id: str,
        file_base64: str = DEFAULT_BASE64, file_name: str = DEFAULT_NAME) -> dict:
        """
        Upload a base64 file and attach it to a card.

        Args:
            card_id (int): The ID of the card.
            field_id (str): The ID of the field to attach the file to.
            file_base64 (str): The base64 encoded file content. Have a default value for test.
            file_name (str): The name of the file. Have a default value for test.
            organization_id (int): The ID of the organization.

        Returns:
            dict: The response from the API.
        """
        return self.attachment_service.upload_and_attach_file(card_id, organization_id, field_id, file_base64, file_name)

    def send_email(self, card_id: int, repo_id: int, from_email: str, subject: str, text: str, to_email: str) -> dict:
        """
        Send an email to a card.

        Args:
            card_id (int): The ID of the card.
            repo_id (int): The ID of the repository.
            from_email (str): The sender's email address.
            subject (str): The subject of the email.
            text (str): The text content of the email.
            to_email (str): The recipient's email address.

        Returns:
            dict: The response from the API.

        """
        return self.email_service.send_email(card_id, repo_id, from_email, subject, text, to_email)

    def send_email_with_attachment(self, card_id: int, repo_id: int, from_email: str,
        subject: str, text: str, organization_id: int,to_email: str, file_base64: str = DEFAULT_BASE64, file_name: str = DEFAULT_NAME) -> dict:
        """
        Send an email with an attachment.

        Args:
            card_id (int): The ID of the card.
            repo_id (int): The ID of the repository.
            from_email (str): The sender's email address.
            subject (str): The subject of the email.
            text (str): The text content of the email.
            to_email (str): The recipient's email address.
            file_base64 (str): The base64 encoded file content. Have a default value for test.
            file_name (str): The name of the file. Have a default value for test.
            organization_id (int): The ID of the organization.

        Returns:
            dict: The response from the API.
        """
        return self.email_service.send_email_with_attachment(card_id, repo_id,
            from_email, subject, text, organization_id, to_email, file_base64, file_name)

    def get_users_from_organization(self, organization_id: int) -> list:
        """
        Get users from an organization.

        Args:
            organization_id (int): The ID of the organization.

        Returns:
            list: The response from the API.
        """
        return self.organization_service.get_users_from_organization(organization_id)

    def get_specific_user_from_organization(self, organization_id: int, email: str) -> dict:
        """
        Get a specific user from an organization.

        Args:
            organization_id (int): The ID of the organization.
            email (str): The email of the user.

        Returns:
            dict: The response from the API.
        """
        return self.organization_service.get_specific_user_from_organization(
            organization_id, email)

    def create_card(self, pipe_id: int, fields: [FieldAttribute]) -> dict:
        """
        Create a card.

        Args:
            pipe_id (int): The ID of the pipe.
            fields (List[FieldAttribute]): The fields of the card. Example: [FieldAttribute(field_id="name", field_value="value")]

        Returns:
            dict: The response from the API.
        """
        return self.card_service.create_card(pipe_id, fields)

    def delete_card(self, card_id: int) -> dict:
        """
        Delete a card.

        Args:
            card_id (int): The ID of the card.

        Returns:
            dict: The response from the API.
        """
        return self.card_service.delete_card(card_id)

if __name__ == "__main__":
    pipefy_sdk = PipefySDK(token="your_token", url="https://api.pipefy.com/graphql")










