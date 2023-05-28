from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.dialects.postgresql import insert as _insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as _select
from sqlalchemy import update as _update
from sqlalchemy import exc as sa_exc

from ..service.fastapi_custom import generate_openapi_responses
from ..service import exceptions as exc
from ..service.roles import Roles
from ..service import models as m
from ..service.dependencies import (
    AccessJWTCookie,
    CheckRoles,
    get_session
)
from ..service.pd_models import (
    interview,
    interview_stage_result
)
from ..service.tokens import (
    AccessToken,
)

from . import schemas as sch


router = APIRouter(tags=['interviews'], prefix='/interviews')


@router.get('',
            responses=generate_openapi_responses(
                exc.InvalidRequestError,
                exc.InvalidTokenError,
                exc.ExpiredTokenError,
                exc.InvalidClientError,
                exc.AccessDenied
                ),
            response_model=sch.GetList.Response.Body,
            dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
            )
async def get_list(query: Query = Depends(sch.GetList.Request.Query),
                   session: AsyncSession = Depends(get_session),
                   at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _select(m.Interview) \
           .join(m.Interview.creator) \
           .join(m.Interview.vacancy) \
           .where(m.Interview.is_deleted == False) \
           .where(m.User.company_id == at.company_id)
    
    if query.creator_id:
        stmt = stmt.filter(m.Interview.creator_id == query.creator_id)
    if query.vacancy_id:
        stmt = stmt.filter(m.Interview.vacancy_id == query.vacancy_id)
    if query.candidate_id:
        stmt = stmt.filter(m.Interview.candidate_id == query.candidate_id)
    if query.stage_code:
        stmt = stmt.filter(m.Interview.stage_code == query.stage_code)
    if query.vacancy_priority_code:
        stmt = stmt.filter(m.Vacancy.priority_code == query.priority_code)
    if query.vacancy_deadline_from:
        stmt = stmt.filter(m.Vacancy.deadline >= query.vacancy_deadline_from)
    if query.vacancy_deadline_to:
        stmt = stmt.filter(m.Vacancy.deadline <= query.vacancy_deadline_to)
    
    res = await session.scalars(stmt)
    interviews = [interview.Read.from_orm(orm_model) for orm_model in res.all()]
    return sch.GetList.Response.Body(interviews=interviews)


@router.get('/{interview_id}',
            responses=generate_openapi_responses(
                exc.InvalidRequestError,
                exc.InvalidTokenError,
                exc.ExpiredTokenError,
                exc.InvalidClientError,
                exc.AccessDenied
                ),
            response_model=sch.Get.Response.Body,
            dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin, Roles.customer))]
            )
async def get_one(interview_id: UUID,
                  session: AsyncSession = Depends(get_session),
                  at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _select(m.Interview) \
           .join(m.Interview.creator) \
           .where(m.User.company_id == at.company_id) \
           .where(m.Interview.id == interview_id) \
           .where(m.Interview.is_deleted == False)
    
    try:
        interview_orm = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    return sch.Get.Response.Body.from_orm(interview_orm)


@router.post('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
             response_model=sch.Create.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
             )
async def create(body: sch.Create.Request.Body,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    
    data_dict = body.dict()
    data_dict['creator_id'] = at.user_id
    data_dict['stage_code'] = 1
    
    stmt = _insert(m.Interview).values(**data_dict).returning(m.Interview.id)
    try:
        interview_id = await session.scalar(stmt)
    except sa_exc.IntegrityError:
        raise exc.InvalidClientError
    return sch.Create.Response.Body(id=interview_id)


@router.delete('/{interview_id}',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError,
                   exc.AccessDenied
                   ),
               response_model=sch.Delete.Response.Body,
               dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
               )
async def delete(interview_id: UUID,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _update(m.Interview) \
           .values(is_deleted=True) \
           .where(m.Interview.id == interview_id) \
           .where(m.Interview.is_deleted == False) \
           .returning(m.Interview.id)
           
    try:
        interview_id = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    return sch.Delete.Response.Body(id=interview_id)


@router.post('/{interview_id}/stage-results',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
             response_model=sch.CreateStageResult.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
             )
async def create_stage_result(interview_id: UUID,
                              body: sch.CreateStageResult.Request.Body,
                              session: AsyncSession = Depends(get_session),
                              at: AccessToken = Depends(AccessJWTCookie())):
    
    data_dict = body.dict()
    data_dict['interview_id'] = interview_id
    data_dict['creator_id'] = at.user_id
    
    stmt = _insert(m.InterviewStageResult).values(**data_dict).returning(m.InterviewStageResult.id)
    
    try:
        interview_stage_result_id = (await session.scalars(stmt)).one()
    except sa_exc.IntegrityError:
        raise exc.InvalidClientError
    
    stmt = _update(m.Interview) \
           .values(stage_code=body.interview_stage_code_new) \
           .where(m.Interview.id == interview_id) \
           .returning(m.Interview.id)
           
    try:
        interview_id = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.CreateStageResult.Response.Body(id=interview_stage_result_id)


@router.get('/{interview_id}/stage-results',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
             response_model=sch.GetStageResultsList.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin, Roles.customer))]
             )
async def get_stage_results_list(interview_id: UUID,
                                 session: AsyncSession = Depends(get_session),
                                 at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _select(m.InterviewStageResult) \
           .join(m.Interview.creator) \
           .where(m.InterviewStageResult.interview_id == interview_id) \
           .where(m.InterviewStageResult.is_deleted == False) \
           .where(m.User.company_id == at.company_id)

    res = await session.scalars(stmt)
    stage_results = [interview_stage_result.Read.from_orm(orm_model) for orm_model in res.all()]
    return sch.GetStageResultsList.Response.Body(stage_results=stage_results)


@router.get('/{interview_id}/stage-results/{stage_result_id}',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
             response_model=sch.GetStageResult.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin, Roles.customer))]
             )
async def get_stage_result(interview_id: UUID,
                           stage_result_id: UUID,
                           session: AsyncSession = Depends(get_session),
                           at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _select(m.InterviewStageResult) \
           .join(m.Interview.creator) \
           .where(m.InterviewStageResult.id == stage_result_id) \
           .where(m.InterviewStageResult.interview_id == interview_id) \
           .where(m.InterviewStageResult.is_deleted == False) \
           .where(m.User.company_id == at.company_id)
    
    try:
        interview_stage_result_orm = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.GetStageResult.Response.Body.from_orm(interview_stage_result_orm)


@router.delete('/{interview_id}/stage-results/{stage_result_id}',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError,
                   exc.AccessDenied
                   ),
               response_model=sch.Delete.Response.Body,
               dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
               )
async def delete_stage_result(interview_id: UUID,
                              stage_result_id: UUID,
                              session: AsyncSession = Depends(get_session),
                              at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _update(m.InterviewStageResult) \
           .values(is_deleted=True) \
           .where(m.InterviewStageResult.id == stage_result_id) \
           .where(m.InterviewStageResult.interview_id == interview_id) \
           .where(m.InterviewStageResult.is_deleted == False) \
           .returning(m.InterviewStageResult.id)
    
    try:
        interview_stage_result_id = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.Delete.Response.Body(id=interview_stage_result_id)
