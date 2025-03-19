import json

class GraphQLMutations:

    @staticmethod
    def mutation_move_card_to_phase(card_id, phase_id) -> str:
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
    def mutation_update_card_field(card_id, field_id=None, new_value=None, fields: [] = []) -> str:
        """Generate a GraphQL mutation to update a card field.

        Args:
            card_id (str): The ID of the card to update.
            field_id (str): The ID of the field to update.
            new_value (str): The new value for the field.
            fields (list): A list of fields to update.

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