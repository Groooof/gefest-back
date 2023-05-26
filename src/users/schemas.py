import typing as tp
from uuid import UUID
from datetime import datetime

import pydantic as pd

    
class Create:
    class Request:
        class Body(pd.BaseModel):
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

            class Config:
                schema_extra = {
                    "title": "CreateRequestBody",
                    "example": {
                        'username': 'user_1',
                        'password': 'qwerty',
                        'role_code': 2,
                        'company_id': '00000000-0000-0000-0000-000000000000',
                        'department_id': None,
                        'position_id': None,
                        'grade_id': None,
                        'first_name': 'Михаил',
                        'last_name': 'Петрович',
                        'middle_name': 'Зубенко',
                        'email': 'pupupu@mail.ru'
                    }
                }
                
    class Response:
        class Body(pd.BaseModel):
            id: UUID

            class Config:
                schema_extra = {
                        "title": "CreateResponseBody",
                        "example": {
                            'id': '6d48cf29-a9ac-45c6-a9e7-85f455b0f361'
                        }
                    }
                
            
class DepartmentInfo(pd.BaseModel):
    id: UUID
    name: str
            
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "DepartmentInfo",
            "example": {
                'id': '00000000-0000-0000-0000-000000000002',
                'name': 'Отдел разработки'
            }
        }
        
class PositionInfo(pd.BaseModel):
    id: UUID
    name: str
            
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "PositionInfo",
            "example": {
                'id': '00000000-0000-0000-0000-000000000005',
                'name': 'Python-developer'
            }
        }
        
        
class GradeInfo(pd.BaseModel):
    id: UUID
    name: str
            
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "PositionInfo",
            "example": {
                'id': '00000000-0000-0000-0000-000000000008',
                'name': 'Junior'
            }
        }
            

class UserInfo(pd.BaseModel):
    id: UUID
    username: str
    role_code: int
    department: tp.Optional[DepartmentInfo]
    position: tp.Optional[PositionInfo]
    grade: tp.Optional[GradeInfo]
    first_name: str
    last_name: str
    middle_name: str
    email: str
    creator_id: tp.Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "title": "UserInfo",
            "example": {
                'id': '00000000-0000-0000-0000-000000000001',
                'username': 'user_1',
                'role_code': 2,
                'department': {
                    'id': '00000000-0000-0000-0000-000000000002',
                    'name': 'Отдел разработки'
                    },
                'position': {
                    'id': '00000000-0000-0000-0000-000000000005',
                    'name': 'Python-developer'
                },
                'grade': {
                    'id': '00000000-0000-0000-0000-000000000008',
                    'name': 'Junior'
                },
                'first_name': 'Михаил',
                'last_name': 'Петрович',
                'middle_name': 'Зубенко',
                'email': 'pupupu@mail.ru'
            }
        }
            
            
class GetSelfInfo:
    class Response:
        class Body(UserInfo):
            ...


class GetUserInfo:
    class Response:
        class Body(UserInfo):
            ...


class GetCompanyUsersInfo:
    class Response:
        class Body(pd.BaseModel):
            users: tp.List[UserInfo]


class DeleteUser:            
    class Response:
        class Body(pd.BaseModel):
            id: UUID

            class Config:
                schema_extra = {
                        "title": "DeleteUserResponseBody",
                        "example": {
                            'id': '6d48cf29-a9ac-45c6-a9e7-85f455b0f361'
                        }
                    }