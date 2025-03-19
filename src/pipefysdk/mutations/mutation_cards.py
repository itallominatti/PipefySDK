import json
from typing import List, Optional, Dict

class GraphQLMutations:

    @staticmethod
    def mutation_move_card_to_phase(card_id: str, phase_id: str) -> str:
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
    def mutation_update_card_field(card_id: str, field_id: Optional[str] = None, new_value: Optional[str] = None, fields: Optional[List[Dict[str, str]]] = None) -> str:
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
    def mutation_create_pre_assigned_url(self,organization_id, filename):
        mutation = """
                    mutation{
                        createPresignedUrl(
                            input: { 
                                organizationId: %(organizationId)s, 
                                fileName: %(fileName)s 
                            }){ url
                        }
                    }
                """ % {
            "organizationId": json.dumps(organization_id),
            "fileName": json.dumps(filename),
        }
        return mutation