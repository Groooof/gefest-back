import typing as tp
from pydantic import BaseModel


class Read(BaseModel):
    code: int
    value: str
    parent_id: tp.Optional[int]
    
    class Config:
        orm_mode = True

