import typing as tp
from uuid import UUID

import pydantic as pd


class Users:
    class Create:
        class Input(pd.BaseModel):
            username: str
            password: str
            role_code: int
            company_id: UUID
            department_id: tp.Optional[UUID]
            position_id: tp.Optional[UUID]
            grade_id: tp.Optional[UUID]
            first_name: str
            last_name: str
            middle_name: str
            email: str
            creator_id: tp.Optional[UUID]
            
        class Output(pd.BaseModel):
            id: UUID
            
    class Verify:
        class Input(pd.BaseModel):
            username: str
            password: str
            
        class Output(pd.BaseModel):
            id: UUID
            role_code: int
            role_sys_name: str

    class GetInfoById:
        class Input(pd.BaseModel):
            id: UUID
            
        class Output(pd.BaseModel):
            username: str
            role_code: int
            company_id: UUID
            department_id: tp.Optional[UUID]
            position_id: tp.Optional[UUID]
            grade_id: tp.Optional[UUID]
            first_name: str
            last_name: str
            middle_name: str
            email: str
            creator_id: tp.Optional[UUID]
