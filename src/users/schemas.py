import typing as tp
from uuid import UUID

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
                
            
class UserInfo(pd.BaseModel):
    id: UUID
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

    class Config:
        orm_mode = True
        schema_extra = {
            "title": "UserInfo",
            "example": {
                'id': '00000000-0000-0000-0000-000000000001',
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