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
                        'company_id': 'a35302aa-b092-4b30-a384-464ed29619e1',
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
                
            
class Read:
    class Response:
        class Body(pd.BaseModel):
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
                schema_extra = {
                    "title": "ReadRequestBody",
                    "example": {
                        'username': 'user_1',
                        'password': 'qwerty',
                        'role_code': 2,
                        'company_id': 'a35302aa-b092-4b30-a384-464ed29619e1',
                        'department_id': None,
                        'position_id': None,
                        'grade_id': None,
                        'first_name': 'Михаил',
                        'last_name': 'Петрович',
                        'middle_name': 'Зубенко',
                        'email': 'pupupu@mail.ru'
                    }
                }


class Delete:            
    class Response:
        class Body(pd.BaseModel):
            id: UUID

            class Config:
                schema_extra = {
                        "title": "DeleteResponseBody",
                        "example": {
                            'id': '6d48cf29-a9ac-45c6-a9e7-85f455b0f361'
                        }
                    }