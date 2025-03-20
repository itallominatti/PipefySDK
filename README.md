```markdown
# PipefySDK

PipefySDK is a Python SDK for interacting with the Pipefy API. It provides a set of methods to manage cards, fields, attachments, and more.

## Installation

You can install the package using `pip` or `poetry`:

```sh
pip install pipefysdk
poetry add pipefysdk
```

## Usage

### Importing the SDK

To use the SDK, you need to import the `PipefySDK` class and initialize it with your Pipefy token and URL.

```python
from pipefysdk import PipefySDK

token = "your_token"  # You don't need to include "Bearer"
url = "https://api.pipefy.com/graphql"
pipefy_sdk = PipefySDK(token=token, url=url)
```

### Methods

#### Get Card Information

Retrieve information about a specific card by its ID.

```python
card_info = pipefy_sdk.get_card_info(card_id=12345)
print(card_info)
```

#### Update a Single Card Field

Update a specific field of a card.

```python
response = pipefy_sdk.update_single_card_field(card_id="12345", field_id="field_id", new_value="new_value")
print(response)
```

#### Update Multiple Card Fields

Update multiple fields of a card.

```python
fields = [{"field_id": "field_id1", "new_value": "value1"}, {"field_id": "field_id2", "new_value": "value2"}]
response = pipefy_sdk.update_multiple_card_fields(card_id="12345", fields=fields)
print(response)
```

#### Search Value in a Field

Search for a value in a specific field of a card.

```python
value = pipefy_sdk.search_value_in_field(card_id=12345, field_id="field_id")
print(value)
```

#### Search Multiple Values in Fields

Search for values in multiple fields of a card.

```python
field_ids = ["field_id1", "field_id2"]
values = pipefy_sdk.search_multiple_values_in_fields(card_id=12345, field_ids=field_ids)
print(values)
```

#### Move Card to a New Phase

Move a card to a different phase.

```python
response = pipefy_sdk.move_card_to_phase(new_phase_id=67890, card_id=12345)
print(response)
```

#### Get Attachments from a Card

Retrieve attachments from a specific card.

```python
attachments = pipefy_sdk.get_attachments_from_card(card_id=12345)
print(attachments)
```

#### Set Assignee in a Card

Set the assignee(s) for a specific card.

```python
assignee_ids = [111, 222]
response = pipefy_sdk.set_assignee_in_card(card_id=12345, assignee_ids=assignee_ids)
print(response)
```

### Upload Attachment to a Card

Upload an attachment to a specific card.

```python
card_id = 12345
field_id = "field_id"
file_base64 = "base64_encoded_file"
file_name = "file_name.png"
organization_id = 67890

response = pipefy_sdk.upload_attachment_to_card(card_id=card_id, field_id=field_id, file_base64=file_base64, file_name=file_name, organization_id=organization_id)
print(response)
```

### Send Email

Send an email to a specific user.

```python
card_id = 12345
from_email = "teste@gmail.com"
repo_id = 67890
subject = "Teste"
text = "Teste"
to_email = "teste2@gmail.com

response = pipefy_sdk.send_email(card_id=card_id, from_email=from_email, repo_id=repo_id, subject=subject, text=text, to_email=to_email)
print(response)
```




## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
```