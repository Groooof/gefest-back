from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..service.fastapi_custom import generate_openapi_responses
from ..service import exceptions as exc
from ..service import models as m
from ..service.dependencies import (
    AccessJWTCookie,
    get_session
)
from ..service.tokens import (
    AccessToken,
)

from . import schemas as sch


router = APIRouter(tags=['refs'], prefix='/refs')


@router.get('/roles',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRolesResponse
             )
async def roles(session: AsyncSession = Depends(get_session),
                at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.RoleRef))
    return sch.GetRolesResponse(roles=[sch.RoleRef.from_orm(orm_model) for orm_model in res.all()])


@router.get('/vacancy-priorities',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def vacancy_priorities(session: AsyncSession = Depends(get_session),
                             at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.VacancyPriorityRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/addresses',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def adresses(session: AsyncSession = Depends(get_session),
                   at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.AdressRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/countries',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def countries(session: AsyncSession = Depends(get_session),
                    at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.CountryRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/family-stats',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def family_stats(session: AsyncSession = Depends(get_session),
                       at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.FamilyStatusRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/contact-types',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def contact_types(session: AsyncSession = Depends(get_session),
                        at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.ContactTypeRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/languages',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def languages(session: AsyncSession = Depends(get_session),
                    at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.LanguageRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/language-levels',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def language_levels(session: AsyncSession = Depends(get_session),
                          at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.LanguageLevelRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/interview-stages',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def interview_stages(session: AsyncSession = Depends(get_session),
                           at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.InterviewStageRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])


@router.get('/vacancy-stats',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRefsResponse
             )
async def vacancy_stats(session: AsyncSession = Depends(get_session),
                        at: AccessToken = Depends(AccessJWTCookie())):
    
    res = await session.scalars(select(m.VacansyStatusRef))
    return sch.GetRefsResponse(data=[sch.Ref.from_orm(orm_model) for orm_model in res.all()])
