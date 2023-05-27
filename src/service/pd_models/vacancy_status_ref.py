from pydantic import BaseModel


class Read(BaseModel):
    code: int
    value: str
    
    class Config:
        orm_mode = True

