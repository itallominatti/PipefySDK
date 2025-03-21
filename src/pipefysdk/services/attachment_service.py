import base64
import binascii
import httpx

from ..utils.constraints import DEFAULT_BASE64, DEFAULT_NAME

class AttachmentService:
    def __init__(self, request_func, queries, mutations):
        self._request = request_func
        self._mutations = mutations
        self._queries = queries

    def upload_and_attach_file(self, card_id: int, organization_id: int, field_id: str,
        file_base64: str = DEFAULT_BASE64, file_name: str = DEFAULT_NAME) -> dict:

        try:
            file_bytes = base64.b64decode(file_base64)
        except binascii.Error:
            raise ValueError("Invalid base64 file content")

        mutation = self._mutations.mutation_create_pre_assigned_url(organization_id, file_name)
        response = self._request(mutation)

        if 'errors' in response:
            raise PermissionError("You need to be on the enterprise plan to use this feature")

        presigned_url = response['data']['createPresignedUrl']['url']

        upload_response = httpx.put(presigned_url, content=file_bytes, headers={'Content-Type': 'application/pdf'})
        upload_response.raise_for_status()

        path_to_send = presigned_url.split('.com/')[1].split('?')[0]

        mutation = self._mutations.mutation_update_card_field(card_id, field_id, path_to_send)
        attach_response = self._request(mutation)
        return attach_response