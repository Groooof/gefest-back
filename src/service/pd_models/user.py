from uuid import UUID
from datetime import datetime, date
import typing as tp

from pydantic import BaseModel, Field

from .department import Read as DepartmentRead
from .position import Read as PositionRead
from .grade import Read as GradeRead


class Read(BaseModel):
    id: UUID
    username: str
    role_code: int
    department: tp.Optional[DepartmentRead]
    position: tp.Optional[PositionRead]
    grade: tp.Optional[GradeRead]
    first_name: str
    last_name: str
    middle_name: str
    email: str
    creator_id: tp.Optional[UUID]
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class Create(BaseModel):
    username: str
    password: str
    role_code: int
    department_id: tp.Optional[UUID]
    position_id: tp.Optional[UUID]
    grade_id: tp.Optional[UUID]
    first_name: str
    last_name: str
    middle_name: tp.Optional[str]
    email: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "UserCreate",
            "example": {
                'username': 'user_1',
                'password': 'qwerty',
                'role_code': 2,
                'department_id': '00000000-0000-0000-0000-000000000002',
                'position_id': '00000000-0000-0000-0000-000000000005',
                'grade_id': '00000000-0000-0000-0000-000000000009',
                'first_name': 'Михаил',
                'last_name': 'Петрович',
                'middle_name': 'Зубенко',
                'email': 'pupupu@mail.ru'
            }
        }
    
class Update(BaseModel):
    id: tp.Optional[UUID]
    username: tp.Optional[str]
    password: tp.Optional[str]
    role_code: tp.Optional[int]
    department_id: tp.Optional[UUID]
    position_id: tp.Optional[UUID]
    grade_id: tp.Optional[UUID]
    first_name: tp.Optional[str]
    last_name: tp.Optional[str]
    middle_name: tp.Optional[str]
    email: tp.Optional[str]
