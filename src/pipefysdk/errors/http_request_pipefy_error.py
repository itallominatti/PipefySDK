class HttpRequestPipefyError(Exception):
    """
     Error classes for HTTP requests to Pipefy API.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message



