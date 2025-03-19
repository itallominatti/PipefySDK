class GraphQLMutations:
    
    @staticmethod
    def mutation_move_card_to_phase(card_id: int, phase_id: int):
        """
        """
        mutation = f"""
            mutation {{
                moveCardToPhase(
                    input: {{
                    
                    }}
                ) {{
                    id
                }}
            }}
        """
        return mutation