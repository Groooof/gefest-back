from pydantic import BaseModel


class Read(BaseModel):
    code: int
    level_code: str
    value: str

    class Config:
        orm_mode = True
