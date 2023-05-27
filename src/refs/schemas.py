import pydantic as pd
from uuid import UUID
import typing as tp


class Ref(pd.BaseModel):
    code: int
    value: str
    parent_id: tp.Optional[int]

    class Config:
        orm_mode = True


class RoleRef(pd.BaseModel):
    code: int
    name: str
    sys_name: str
    
    class Config:
        orm_mode = True
    
    
class GetRefsResponse(pd.BaseModel):
    data: tp.List[Ref]
    
    
class GetRolesResponse(pd.BaseModel):
    roles: tp.List[RoleRef]
    
