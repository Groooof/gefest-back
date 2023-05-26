from datetime import datetime, date
from uuid import UUID
import typing as tp

from pydantic import BaseModel, Field


class Candidate(BaseModel):
    position_id: tp.Optional[UUID]
    first_name: str
    last_name: str
    middle_name: tp.Optional[str]
    birth_date: tp.Optional[date]
    min_salary: tp.Optional[int]
    adress_code: tp.Optional[int]
    citizenship_code: tp.Optional[int]
    family_status_code: int
    grade_id: tp.Optional[UUID]
    
    class Config:
        schema_extra = {
            "title": "Candidate",
            "example": {
                'position_id': '00000000-0000-0000-0000-000000000005',
                'first_name': 'Алексей',
                'last_name': 'Дубенко',
                'middle_name': None,
                'birth_date': '2002-02-14',
                'min_salary': 75000,
                'adress_code': 33,
                'citizenship_code': 1,
                'family_status_code': 1,
                'grade_id': '00000000-0000-0000-0000-000000000009'
            }
        }
    

class Contact(BaseModel):
    type_code: int
    value: str
    is_priority: tp.Optional[bool] = False
    
    class Config:
        schema_extra = {
            "title": "Contact",
            "example": {
                'type_code': 1,
                'value': '79781112233',
                'is_priority': False
            }
        }
        
    
class Expirience(BaseModel):
    position: str
    company: str
    work_from: date
    work_to: tp.Optional[date]
    is_actual: tp.Optional[bool] = False
    
    class Config:
        schema_extra = {
            "title": "Expirience",
            "example": {
                'position': 'Сеньер помидор',
                'company': 'SpaceX',
                'work_from': '2019-01-01',
                'work_to': '2020-03-14',
                'is_actual': False
            }
        }
    
    
class Language(BaseModel):
    language_code: int
    language_level_code: int
    
    class Config:
        schema_extra = {
            "title": "Language",
            "example": {
                'language_code': 2,
                'language_level_code': 4
            }
        }
    

class NewSkill(BaseModel):
    name: str
    
    class Config:
        schema_extra = {
            "title": "NewSkill",
            "example": {
                'name': 'GiT Hub'
            }
        }
        

class ExistingSkill(BaseModel):
    skill_id: UUID
    
    class Config:
        schema_extra = {
            "title": "ExistingSkill",
            "example": {
                'skill_id': '00000000-0000-0000-0000-000000000012'
            }
        }
    

class PositionInfo(BaseModel):
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


class GradeInfo(BaseModel):
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


class FamilyStatusInfo(BaseModel):
    code: int
    value: str
            
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "FamilyStatusInfo",
            "example": {
                'code': 1,
                'value': 'Single'
            }
        }
        
        
class CountryInfo(BaseModel):
    code: int
    value: str
            
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "CountryInfo",
            "example": {
                'code': 1,
                'value': 'Российская Федерация'
            }
        }
        
    
class ContactInfo(BaseModel):
    type_code: int
    value: str
    is_priority: tp.Optional[bool] = False
    creator_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "ContactInfo",
            "example": {
                'type_code': 1,
                'value': '79781112233',
                'is_priority': False,
                'creator_id': '00000000-0000-0000-0000-000000000001',
                'created_at': '2023-01-01T12:00',
            }
        }


class LanguageInfo(BaseModel):
    code: int
    value: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "LanguageInfo",
            "example": {
                'code': 2,
                'value': 'Английский'
            }
        }
        
    
class LanguageLevelInfo(BaseModel):
    code: int
    level_code: str
    value: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "LanguageLevelInfo",
            "example": {
                'code': 2,
                'level_code': 'B1',
                'value': 'Средний'
            }
        }


class LanguageInfo(BaseModel):
    code: int
    value: str
            
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "LanguageInfo",
            "example": {
                'code': 1,
                'value': 'Российская Федерация'
            }
        }


class LanguageFullInfo(BaseModel):
    id: UUID
    language: LanguageInfo
    language_level: LanguageLevelInfo
    creator_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True


class NotesInfo(BaseModel):
    id: UUID
    note: str
    creator_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "title": "NotesInfo",
            "example": {
                'id': '00000000-0000-0000-0000-000000000099',
                'note': 'Пу пу пу...',
                'creator_id': '00000000-0000-0000-0000-000000000001',
                'created_at': '2023-01-01T12:00',
            }
        }
        

class SkillInfo(BaseModel):
    normalized_name: str
    
    class Config:
        orm_mode = True


class SkillFullInfo(BaseModel):
    id: UUID
    skill: SkillInfo
    creator_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        

class AdressInfo(BaseModel):
    code: int
    value: str

    class Config:
        orm_mode = True


class WorkExpirienceInfo(BaseModel):
    id: UUID
    position: str
    company: str
    work_from: date
    work_to: tp.Optional[date]
    is_actual: tp.Optional[bool] = False
    creator_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class CandidateInfo(BaseModel):
    id: UUID
    creator_id: UUID
    created_at: datetime
    first_name: str
    last_name: str
    middle_name: tp.Optional[str]
    birth_date: tp.Optional[date]
    min_salary: tp.Optional[int]
    adress: tp.Optional[AdressInfo]
    citizenship: tp.Optional[CountryInfo]
    family_status: tp.Optional[FamilyStatusInfo]
    position: PositionInfo
    grade: GradeInfo
    contacts: tp.List[ContactInfo] = Field(default_factory=list)
    work_expirience: tp.List[WorkExpirienceInfo] = Field(default_factory=list)
    languages: tp.List[LanguageFullInfo] = Field(default_factory=list)
    notes: tp.List[NotesInfo] = Field(default_factory=list)
    skills: tp.List[SkillFullInfo] = Field(default_factory=list)

    class Config:
        orm_mode = True


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


class GetList:
    class Request:
        class Query(BaseModel):
            first_name: tp.Optional[str]
            last_name: tp.Optional[str]
            middle_name: tp.Optional[str]
            position_id: tp.Optional[UUID]
            recruiter_id: tp.Optional[UUID]
            
    
    class Response:
        class Body(BaseModel):
            candidates: tp.List[CandidateInfo] = Field(default_factory=list)
