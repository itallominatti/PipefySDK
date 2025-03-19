from pydantic import BaseModel

class RequestModel(BaseModel):
    query: str
