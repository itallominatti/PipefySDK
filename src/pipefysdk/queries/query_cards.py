class GraphQLQueries:
    @staticmethod
    def search_fields_in_card(card_id: int) -> str:
        """
        Search fields in a card.

        Args:
            card_id (int): ID of the card

        Returns:
            str: GraphQL query string

        """
        query = f"""
        {{
          card(id: "{card_id}") {{
            fields {{
              field {{
                id
              }}
              name
              value
            }}
          }}
        }}
        """
        return query

    @staticmethod
    def value_in_field_exists(pipe_id: int, field_id: str, value: str) -> str:
        """
        Check if a value exists in a field on a pipe.

        Args:
            pipe_id (int): ID of the pipe
            field_id (str): ID of the field
            value (str): Value to check

        Returns:
            str: GraphQL query string
        """
        query = f"""
        query {{
          findCards(
            pipeId: {pipe_id}
            search: {{ fieldId: "{field_id}", fieldValue: "{value}" }}
          ) {{
            edges {{
              node {{
                fields {{
                  date_value
                  datetime_value
                  filled_at
                  float_value
                  indexName
                  name
                  native_value
                  report_value
                  updated_at
                  value
                }}
                title
                id
                current_phase {{
                  id
                }}
                expired
                createdAt
              }}
            }}
          }}
        }}"""
        return query

    @staticmethod
    def get_attachments_from_card(card_id: int) -> str:
        """
        Get attachments from a card.

        Args:
            card_id (int): ID of the card

        Returns:
            str: GraphQL query string
        """
        query = f"""
            {{
              card(id: "{card_id}") {{
                id
                attachments {{
                    field {{
                        id
                        index_name
                    }}
                    path
                    url
                }}
              }}
            }}
            """
        return query