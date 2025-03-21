
from ..errors.card_move_pipefy_error import CardMovePipefyError

class PhaseService:
    def __init__(self, request_func, queries, mutations):
        self._request = request_func
        self._mutations = mutations
        self._queries = queries

    def move_card_to_phase(self, new_phase_id: int, card_id: int) -> dict:
        mutation = self._mutations.mutation_move_card_to_phase(card_id=card_id, phase_id=new_phase_id)
        response = self._request(mutation)
        if 'errors' in response:
            raise CardMovePipefyError(f"{response['errors']}. Probably, you have required fields empty in your card.")
        return response