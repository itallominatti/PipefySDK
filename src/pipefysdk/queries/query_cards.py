class GraphQLQueries:
    
    @staticmethod
    def search_fields_in_card(card_id: int):
        """
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