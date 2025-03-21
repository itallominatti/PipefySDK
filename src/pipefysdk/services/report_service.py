class ReportService:
    def __init__(self, request_func, queries, mutations):
        self._request = request_func
        self._mutations = mutations
        self._queries = queries

