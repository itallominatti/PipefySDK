from pydantic import BaseModel

class FieldAttribute(BaseModel):
    field_id: str
    field_value: str