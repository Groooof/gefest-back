import typing as tp

import pydantic as pd


class RoleInfo(pd.BaseModel):
    code: int
    name: str
    sys_name: str


class Roles:
    class GetAll:
        class Output(pd.BaseModel):
            roles: tp.List[RoleInfo]
