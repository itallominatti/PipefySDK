import base64
import binascii

import httpx

from src.pipefysdk.utils.constraints import DEFAULT_BASE64, DEFAULT_NAME

class EmailService:
    def __init__(self, request_func, queries, mutations):
        self._request = request_func
        self._mutations = mutations
        self._queries = queries

    def send_email(self, card_id: int, repo_id: int, from_email: str,
        subject: str, text: str, to_email: str) -> dict:

        mutation_create_email = self._mutations.mutation_create_inbox_email(card_id,
            repo_id, from_email, subject, text, to_email)
        response_create_email = self._request(mutation_create_email)

        if 'errors' in response_create_email:
            raise RuntimeError(f"Failed to create inbox email: {response_create_email['errors']}")

        email_id = response_create_email['data']['createInboxEmail']['inbox_email']['id']
        mutation_send_email = self._mutations.mutation_send_inbox_email(email_id)
        response_send_email = self._request(mutation_send_email)

        return response_send_email

    def send_email_with_attachment(self, card_id: int, repo_id: int, from_email: str,
        subject: str, text: str, organization_id: int,to_email: str,
        file_base64: str = DEFAULT_BASE64, file_name: str = DEFAULT_NAME) -> dict:

        try:
            file_bytes = base64.b64decode(file_base64)
        except binascii.Error:
            raise ValueError("Invalid base64 file content")

        # Step 1: Generate pre-signed URL
        mutation = self._mutations.mutation_create_pre_assigned_url(organization_id, file_name)
        response = self._request(mutation)

        if 'errors' in response:
            raise PermissionError("You need to be on the enterprise plan to use this feature")

        presigned_url = response['data']['createPresignedUrl']['url']

        # Step 2: Upload the file to the pre-signed URL
        upload_response = httpx.put(presigned_url, content=file_bytes, headers={'Content-Type': 'application/pdf'})
        upload_response.raise_for_status()
        path_to_send = presigned_url.split('.com/')[1].split('?')[0]

        # Step 3: Create the inbox email with the attachment
        mutation_create_email = self._mutations.mutation_create_inbox_email_with_attachment(card_id, repo_id, from_email, subject, text, to_email, path_to_send, file_name)
        response_create_email = self._request(mutation_create_email)

        if 'errors' in response_create_email:
            raise RuntimeError(f"Failed to create inbox email: {response_create_email['errors']}")

        email_id = response_create_email['data']['createInboxEmail']['inbox_email']['id']

        # Step 4: Send the email
        mutation_send_email = self._mutations.mutation_send_inbox_email(email_id)
        response_send_email = self._request(mutation_send_email)

        return response_send_email