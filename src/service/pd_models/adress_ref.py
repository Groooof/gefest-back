from pydantic import BaseModel


class Read(BaseModel):
    code: int
    value: str
    parent_id: int
    
    class Config:
        orm_mode = True

