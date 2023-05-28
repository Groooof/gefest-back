from uuid import UUID
from datetime import datetime, date
import typing as tp

from pydantic import BaseModel, Field

from . import (
    position,
    department,
    grade,
    adress_ref,
    vacancy_skill,
    skill,
    vacancy_priority_ref,
    vacancy_status_ref
)


class Filters(BaseModel):
    recruiter_id: tp.Optional[UUID]
    department_id: tp.Optional[UUID]
    position_id: tp.Optional[UUID]
    grade_id: tp.Optional[UUID]
    priority_code: tp.Optional[int]
    adress_code: tp.Optional[int]
    status_code: tp.Optional[int]
    date_from: tp.Optional[date]
    date_to: tp.Optional[date]
    salary_from: tp.Optional[int]
    salary_to: tp.Optional[int]
    # skills: tp.Optional[tp.List[UUID]]


class Read(BaseModel):
    id: UUID
    position: position.Read
    department: department.Read
    grade: tp.Optional[grade.Read]
    salary_from: tp.Optional[int]
    salary_to: tp.Optional[int]
    employee_count: int
    priority: vacancy_priority_ref.Read
    deadline: tp.Optional[date]
    recruiter_id: tp.Optional[UUID]
    adress: tp.Optional[adress_ref.Read]
    status: vacancy_status_ref.Read
    project: tp.Optional[str]
    skills: tp.List[vacancy_skill.Read] = Field(default_factory=list)
    creator_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class Create(BaseModel):
    position_id: UUID
    department_id: UUID
    grade_id: tp.Optional[UUID]
    employee_count: int
    priority_code: int
    salary_from: tp.Optional[int]
    salary_to: tp.Optional[int]
    deadline: tp.Optional[date]
    adress_code: tp.Optional[int]
    project: tp.Optional[str]
    skills: tp.List[tp.Union[skill.Create, vacancy_skill.Create]] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "title": "VacancyCreate",
            "example": {
                'position_id': '00000000-0000-0000-0000-000000000005',
                'department_id': '00000000-0000-0000-0000-000000000002',
                'grade_id': '00000000-0000-0000-0000-000000000008',
                'employee_count': 1,
                'priority_code': 1,
                'salary_from': 50000,
                'salary_to': 90000,
                'deadline': '2023-06-15',
                'adress_code': 33,
                'project': 'GefestPRO',
                'skills': [
                    skill.Create.Config.schema_extra['example'],
                    vacancy_skill.Create.Config.schema_extra['example']
                ]
            }
        }
        
    def dict_vacancy_only(self):
        return self.dict(exclude={'skills'})
        

class Update(BaseModel):
    position_id: UUID
    department_id: UUID
    grade_id: tp.Optional[UUID]
    employee_count: int
    priority_code: int
    salary_from: tp.Optional[int]
    salary_to: tp.Optional[int]
    deadline: tp.Optional[date]
    adress_code: tp.Optional[int]
    status_code: int
    project: tp.Optional[str]
    recruiter_id: tp.Optional[UUID]
    skills: tp.List[tp.Union[skill.Create, vacancy_skill.Update]] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "title": "VacancyUpdate",
            "example": {
                'position_id': '00000000-0000-0000-0000-000000000005',
                'department_id': '00000000-0000-0000-0000-000000000002',
                'grade_id': '00000000-0000-0000-0000-000000000008',
                'employee_count': 1,
                'priority_code': 1,
                'salary_from': 50000,
                'salary_to': 90000,
                'deadline': '2023-06-15',
                'adress_code': 33,
                'status_code': 1,
                'project': 'GefestPRO',
                'recruiter_id': '00000000-0000-0000-0000-000000000001',
                'skills': [
                    skill.Create.Config.schema_extra['example'],
                    vacancy_skill.Create.Config.schema_extra['example']
                ]
            }
        }
        
    def dict_vacancy_only(self):
        return self.dict(exclude={'skills'})
    
