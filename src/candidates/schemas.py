from datetime import datetime
from uuid import UUID
import typing as tp

from pydantic import BaseModel, Field


class Candidate(BaseModel):
    position: tp.Optional[str]
    first_name: str
    last_name: str
    middle_name: tp.Optional[str]
    birth_date: tp.Optional[datetime]
    salary_minimum: tp.Optional[int]
    adress_code: tp.Optional[int]
    citizenship_code: tp.Optional[int]
    family_status_code: int
    grade_id: tp.Optional[UUID]
    

class Contact(BaseModel):
    type_code: int
    value: str
    is_priority: tp.Optional[bool] = False
    
    
class Expirience(BaseModel):
    position: str
    company: str
    work_from: datetime
    work_to: tp.Optional[datetime]
    is_actual: tp.Optional[bool] = False
    
    
class Language(BaseModel):
    code: int
    level_code: int
    
    
class NewSkill(BaseModel):
    value: str
    
    
class ExistingSkill(BaseModel):
    id: UUID
    
    
class Create:
    class Request:
        class Body(BaseModel):
            candidate: Candidate
            contacts: tp.List[Contact] = Field(default_factory=list)
            expiriense: tp.List[Expirience] = Field(default_factory=list)
            languages: tp.List[Language] = Field(default_factory=list)
            notes: tp.List[str] = Field(default_factory=list)
            skills: tp.List[tp.Union[NewSkill, ExistingSkill]] = Field(default_factory=list)

    class Response:
        class Body(BaseModel):
            id: UUID
