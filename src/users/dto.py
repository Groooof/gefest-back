import typing as tp
from uuid import UUID

import pydantic as pd


class Users:
    class Create:
        class Input(pd.BaseModel):
            username: str
            password: str
            role: str
            is_superuser: bool = False
            
        class Output(pd.BaseModel):
            id: tp.Optional[UUID]
            
    class Verify:
        class Input(pd.BaseModel):
            username: str
            password: str
            
        class Output(pd.BaseModel):
            id: tp.Optional[UUID]
