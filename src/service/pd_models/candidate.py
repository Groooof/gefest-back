from uuid import UUID
from datetime import datetime, date
import typing as tp

from pydantic import BaseModel, Field

from . import (
    position,
    grade,
    adress,
    country,
    family_status,
    contact,
    work_place,
    candidate_language,
    candidate_note,
    candidate_skill,
    skill
)


class Read(BaseModel):
    id: UUID
    creator_id: UUID
    created_at: datetime
    first_name: str
    last_name: str
    middle_name: tp.Optional[str]
    birth_date: tp.Optional[date]
    min_salary: tp.Optional[int]
    adress: tp.Optional[adress.Read]
    citizenship: tp.Optional[country.Read]
    family_status: tp.Optional[family_status.Read]
    position: position.Read
    grade: grade.Read
    contacts: tp.List[contact.Read] = Field(default_factory=list)
    work_places: tp.List[work_place.Read] = Field(default_factory=list)
    languages: tp.List[candidate_language.Read] = Field(default_factory=list)
    notes: tp.List[candidate_note.Read] = Field(default_factory=list)
    skills: tp.List[candidate_skill.Read] = Field(default_factory=list)
    
    class Config:
        orm_mode = True


class Create(BaseModel):
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
    contacts: tp.List[contact.Create] = Field(default_factory=list)
    work_places: tp.List[work_place.Create] = Field(default_factory=list)
    languages: tp.List[candidate_language.Create] = Field(default_factory=list)
    notes: tp.List[candidate_note.Create] = Field(default_factory=list)
    skills: tp.List[tp.Union[skill.Create, candidate_skill.Create]] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "title": "CandidateCreate",
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
                'grade_id': '00000000-0000-0000-0000-000000000009',
                'contacts': [contact.Create.Config.schema_extra['example']],
                'work_places': [work_place.Create.Config.schema_extra['example']],
                'languages': [candidate_language.Create.Config.schema_extra['example']],
                'notes': [candidate_note.Create.Config.schema_extra['example']],
                'skills': [
                    skill.Create.Config.schema_extra['example'],
                    candidate_skill.Create.Config.schema_extra['example']
                ]
            }
        }
        
    def dict_candidate_only(self):
        return self.dict(exclude={'contacts', 'work_places', 'languages', 'notes', 'skills'})
