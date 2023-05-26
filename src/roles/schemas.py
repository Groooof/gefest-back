import typing as tp
import pydantic as pd

    
class RoleInfo(pd.BaseModel):
    code: int
    name: str
    sys_name: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "code": "1",
                "name": "Администратор",
                "sys_name": 'admin'
            }
        }
    
class GetRoles:
    class Response:
        class Body(pd.BaseModel):
            roles: tp.List[RoleInfo]
            
            class Config:
                schema_extra = {
                    "title": "GetRolesResponseBody"
                }
    