class CardCreatePipefyError(Exception):
    def __init__(self, errors):
        if isinstance(errors, str):
            errors = [{'message': errors}]
        self.errors = errors
        super().__init__(self._format_message())

    def _format_message(self):
        error_messages = [error['message'] for error in self.errors]
        return f"CardCreatePipefyError: {', '.join(error_messages)}"