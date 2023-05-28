from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc as sa_exc

from ..service import models as m
from ..service.dependencies import (
    AccessJWTCookie,
    get_session
)

from . import schemas as sch
from ..service.tokens import (
    AccessToken,
)

from ..service import exceptions as exc
from ..service.fastapi_custom import generate_openapi_responses

from ..service.pd_models import interview, interview_stage_result


router = APIRouter(tags=['interviews'], prefix='/interviews')


@router.get('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetList.Response.Body
             )
async def get_list(query: Query = Depends(sch.GetList.Request.Query),
                   session: AsyncSession = Depends(get_session),
                   at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = select(m.Interview) \
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
    return sch.GetList.Response.Body(
        interviews=[interview.Read.from_orm(orm_model) for orm_model in res.all()]
    )


@router.get('/{interview_id}',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.Get.Response.Body
             )
async def get(interview_id: UUID,
              session: AsyncSession = Depends(get_session),
              at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = select(m.Interview) \
           .join(m.Interview.creator) \
           .where(
               (m.User.company_id == at.company_id)
               &
               (m.Interview.id == interview_id)
               &
               (m.Interview.is_deleted == False)
            )
    res = await session.scalars(stmt)
    try:
        interview_orm = res.one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    return sch.Get.Response.Body.from_orm(interview_orm)


@router.post('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.Create.Response.Body
             )
async def create(body: sch.Create.Request.Body,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    
    data_dict = body.dict()
    data_dict['creator_id'] = at.user_id
    data_dict['stage_code'] = 1
    
    stmt = insert(m.Interview).values(**data_dict).returning(m.Interview.id)
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
                   exc.InvalidClientError
                   ),
               response_model=sch.Delete.Response.Body
               )
async def delete_interview(interview_id: UUID,
                           session: AsyncSession = Depends(get_session),
                           at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = update(m.Interview) \
           .values(is_deleted=True) \
           .where(
               (m.Interview.id == interview_id)
               &
               (m.Interview.is_deleted == False)
           ) \
           .returning(m.Interview.id)
    res = await session.scalars(stmt)
    try:
        interview_id = res.one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    return sch.Delete.Response.Body(id=interview_id)


@router.post('/{interview_id}/stage-results',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.CreateStageResult.Response.Body
             )
async def create_stage_result(interview_id: UUID,
                              body: sch.CreateStageResult.Request.Body,
                              session: AsyncSession = Depends(get_session),
                              at: AccessToken = Depends(AccessJWTCookie())):
    
    data_dict = body.dict()
    data_dict['interview_id'] = interview_id
    data_dict['creator_id'] = at.user_id
    
    stmt = insert(m.InterviewStageResult).values(**data_dict).returning(m.InterviewStageResult.id)
    
    res = await session.scalars(stmt)
    try:
        interview_stage_result_id = res.one()
    except sa_exc.IntegrityError:
        raise exc.InvalidClientError
    
    stmt = update(m.Interview) \
           .values(stage_code=body.interview_stage_code_new) \
           .where(m.Interview.id == interview_id) \
           .returning(m.Interview.id)
           
    res = await session.scalars(stmt)
    try:
        interview_id = res.one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.CreateStageResult.Response.Body(id=interview_stage_result_id)


@router.get('/{interview_id}/stage-results',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetStageResultsList.Response.Body
             )
async def get_stage_results_list(interview_id: UUID,
                                 session: AsyncSession = Depends(get_session),
                                 at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = select(m.InterviewStageResult) \
           .join(m.Interview.creator) \
           .where(m.InterviewStageResult.interview_id == interview_id) \
           .where(m.InterviewStageResult.is_deleted == False) \
           .where(m.User.company_id == at.company_id)
    

    res = await session.scalars(stmt)
    return sch.GetStageResultsList.Response.Body(
        stage_results=[interview_stage_result.Read.from_orm(orm_model) for orm_model in res.all()]
    )


@router.get('/{interview_id}/stage-results/{stage_result_id}',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetStageResult.Response.Body
             )
async def get_stage_result(interview_id: UUID,
                           stage_result_id: UUID,
                           session: AsyncSession = Depends(get_session),
                           at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = select(m.InterviewStageResult) \
           .join(m.Interview.creator) \
           .where(m.InterviewStageResult.id == stage_result_id) \
           .where(m.InterviewStageResult.interview_id == interview_id) \
           .where(m.InterviewStageResult.is_deleted == False) \
           .where(m.User.company_id == at.company_id)
    

    res = await session.scalars(stmt)
    try:
        interview_stage_result_orm = res.one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.GetStageResult.Response.Body.from_orm(interview_stage_result_orm)


@router.delete('/{interview_id}/stage-results/{stage_result_id}',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError
                   ),
               response_model=sch.Delete.Response.Body
               )
async def delete_stage_result(interview_id: UUID,
                              stage_result_id: UUID,
                              session: AsyncSession = Depends(get_session),
                              at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = update(m.InterviewStageResult) \
           .values(is_deleted=True) \
           .where(m.InterviewStageResult.id == stage_result_id) \
           .where(m.InterviewStageResult.interview_id == interview_id) \
           .where(m.InterviewStageResult.is_deleted == False) \
           .returning(m.InterviewStageResult.id)
    
    res = await session.scalars(stmt)
    try:
        interview_stage_result_id = res.one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.Delete.Response.Body(id=interview_stage_result_id)


