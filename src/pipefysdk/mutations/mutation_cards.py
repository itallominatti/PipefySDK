import json
from typing import List, Optional, Dict

from src.pipefysdk.models.models import FieldAttribute

class GraphQLMutations:

    @staticmethod
    def mutation_move_card_to_phase(card_id: int, phase_id: int) -> str:
        """Generate a GraphQL mutation to move a card to a new phase.

        Args:
            card_id (str): The ID of the card to move.
            phase_id (str): The ID of the destination phase.

        Returns:
            str: The GraphQL mutation string.
        """
        mutation = f'''
        mutation {{
          moveCardToPhase(
            input: {{
              card_id: {json.dumps(card_id)}
              destination_phase_id: {json.dumps(phase_id)}
            }}
          ) {{
            card {{
              id
              current_phase {{
                name
              }}
            }}
          }}
        }}
        '''
        return mutation

    @staticmethod
    def mutation_update_card_field(card_id: int, field_id: Optional[str] = None, new_value: Optional[str] = None, fields: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate a GraphQL mutation to update a card field.

        Args:
            card_id (str): The ID of the card to update.
            field_id (Optional[str]): The ID of the field to update.
            new_value (Optional[str]): The new value for the field.
            fields (Optional[List[Dict[str, str]]]): A list of fields to update.

        Returns:
            str: The GraphQL mutation string.
        """
        if fields:
            values = ', '.join([
                f'{{fieldId: {json.dumps(field["field_id"])}, value: {json.dumps(field["new_value"])}}}'
                for field in fields
            ])
        else:
            values = f'{{fieldId: {json.dumps(field_id)}, value: {json.dumps(new_value)}}}'

        mutation = f'''
        mutation {{
          updateFieldsValues(
            input: {{
              nodeId: {json.dumps(card_id)}
              values: [{values}]
            }}
          ) {{
            success
            userErrors {{
              field
              message
            }}
            updatedNode {{
              __typename
            }}
          }}
        }}
        '''
        return mutation

    @staticmethod
    def update_card_assignee(card_id: int, assignee_ids: list) -> str:
        """
        Update the assignee of a card.

        Args:
            card_id (int): ID of the card
            assignee_ids (list): List of assignee IDs

        Returns:
            str: GraphQL mutation string
        """
        assignee_ids_str = ', '.join(f'"{id}"' for id in assignee_ids)
        mutation = f"""
            mutation {{
              updateCard(input: {{
                id: "{card_id}",
                assignee_ids: [{assignee_ids_str}]
              }}) {{
                card {{
                  id
                  title
                }}
              }}
            }}
            """
        return mutation

    @staticmethod
    def mutation_create_pre_assigned_url(organization_id: int, filename: str) -> str:
        """Generate a GraphQL mutation to create a pre-signed URL."""
        mutation = """
            mutation {
              createPresignedUrl(
                input: { 
                  organizationId: %(organizationId)s, 
                  fileName: %(fileName)s 
                }) { url
              }
            }
            """ % {
            "organizationId": json.dumps(organization_id),
            "fileName": json.dumps(filename),
        }
        return mutation

    @staticmethod
    def mutation_create_inbox_email(card_id: int, repo_id: int, from_email: str, subject: str, text: str,
                                    to_email: str) -> str:
        """Generate a GraphQL mutation to create an inbox email.

        Args:
            card_id (int): The ID of the card.
            repo_id (int): The ID of the repository.
            from_email (str): The sender's email address.
            subject (str): The subject of the email.
            text (str): The text content of the email.
            to_email (str): The recipient's email address.

        Returns:
            str: The GraphQL mutation string.
        """
        mutation = f'''
           mutation {{
             createInboxEmail(input: {{
               card_id: {json.dumps(card_id)},
               repo_id: {json.dumps(repo_id)},
               from: {json.dumps(from_email)},
               subject: {json.dumps(subject)},
               text: {json.dumps(text)},
               to: {json.dumps(to_email)}
             }}) {{
               inbox_email {{
                 id
                 state
               }}
             }}
           }}
           '''
        return mutation

    @staticmethod
    def mutation_send_inbox_email(email_id: str) -> str:
        """Generate a GraphQL mutation to send an inbox email.

        Args:
            email_id (str): The ID of the inbox email.

        Returns:
            str: The GraphQL mutation string.
        """
        mutation = f'''
           mutation {{
             sendInboxEmail(input: {{
               id: {json.dumps(email_id)}
             }}) {{
               clientMutationId
               success
             }}
           }}
           '''
        return mutation

    @staticmethod
    def mutation_create_inbox_email_with_attachment(card_id: int, repo_id: int, from_email: str, subject: str,
                                                    text: str, to_email: str, file_url: str, file_name: str) -> str:
        """Generate a GraphQL mutation to create an inbox email with an attachment.

        Args:
            card_id (int): The ID of the card.
            repo_id (int): The ID of the repository.
            from_email (str): The sender's email address.
            subject (str): The subject of the email.
            text (str): The text content of the email.
            to_email (str): The recipient's email address.
            file_url (str): The URL of the file.
            file_name (str): The name of the file.

        Returns:
            str: The GraphQL mutation string.
        """
        mutation = f'''
           mutation {{
             createInboxEmail(input: {{
               card_id: {json.dumps(card_id)},
               repo_id: {json.dumps(repo_id)},
               from: {json.dumps(from_email)},
               subject: {json.dumps(subject)},
               text: {json.dumps(text)},
               to: {json.dumps(to_email)},
               emailAttachments: [{{
                 fileUrl: {json.dumps(file_url)},
                 fileName: {json.dumps(file_name)}
               }}]
             }}) {{
               inbox_email {{
                 id
                 state
               }}
             }}
           }}
           '''
        return mutation

    @staticmethod
    def mutation_create_card(pipe_id: int, fields_attributes: List[FieldAttribute]) -> str:
        mutation = f"""       
                mutation {{           
                createCard(input: {{               
                    pipe_id: {pipe_id},               
                       fields_attributes: [                    
                              {', '.join([f'{{field_id: "{field.field_id}", field_value: "{field.field_value}"}}'
                                          for field in fields_attributes])}      
                      ]            }}) 
                      {{                
                           clientMutationId
                                    card {{
                                id                
                }}            
            }}        
            }}        
            """
        return mutation

    @staticmethod
    def mutation_delete_card(card_id: int) -> str:
        """Generate a GraphQL mutation to delete a card.

        Args:
            card_id (int): The ID of the card.

        Returns:
            str: The GraphQL mutation string.
        """
        mutation = f'''
           mutation {{
             deleteCard(input: {{
               card_id: {json.dumps(card_id)}
             }}) {{
               success
               clientMutationId
             }}
           }}
           '''
        return mutation


