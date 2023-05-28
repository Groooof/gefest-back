from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.dialects.postgresql import insert

from . import mocks
from . import models as m


class MocksLoader:
    def __init__(self, conn: AsyncConnection) -> None:
        self._conn = conn

    async def load(self):
        await self._load(mocks.companies, m.Company)
        await self._load(mocks.departments, m.Department)
        await self._load(mocks.positions, m.Position)
        await self._load(mocks.grades, m.Grade)
        await self._load(mocks.users, m.User)
        await self._load(mocks.skills, m.Skill)
        await self._load(mocks.candidates, m.Candidate)
        await self._load(mocks.candidate_contacts, m.CandidateContact)
        await self._load(mocks.candidate_work_places, m.CandidateWorkPlace)
        await self._load(mocks.candidate_languages, m.CandidateLanguageAbility)
        await self._load(mocks.candidate_notes, m.CandidateNote)
        await self._load(mocks.candidate_skills, m.CandidateSkill)
        await self._load(mocks.vacancies, m.Vacancy)
        await self._load(mocks.vacancy_skills, m.VacancySkill)
        await self._load(mocks.interviews, m.Interview)
        await self._load(mocks.interview_stage_results, m.InterviewStageResult)
        
    async def _load(self, data: list, sa_model: DeclarativeMeta):
        stmt = insert(sa_model).values(data).on_conflict_do_nothing()
        await self._conn.execute(stmt)
