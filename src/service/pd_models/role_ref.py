from pydantic import BaseModel


class Read(BaseModel):
    code: int
    name: str
    sys_name: str
    
    class Config:
        orm_mode = True

