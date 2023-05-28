from uuid import UUID
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.dialects.postgresql import insert as _insert
from sqlalchemy.future import select as _select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete as _delete
from sqlalchemy.orm import exc as sa_exc

from ..service.fastapi_custom import generate_openapi_responses
from ..service import exceptions as exc
from ..service.pd_models import grade
from ..service import models as m
from ..service.dependencies import (
    AccessJWTCookie,
    get_session
)
from ..service.tokens import (
    AccessToken,
)

from . import schemas as sch


router = APIRouter(tags=['grades'], prefix='/grades')


@router.get('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetList.Response.Body
             )
async def get_list(session: AsyncSession = Depends(get_session),
                   at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _select(m.Grade).where(m.Grade.company_id == at.company_id)
    res = await session.scalars(stmt)
    grades = [grade.Read.from_orm(orm_model) for orm_model in res.all()]
    return sch.GetList.Response.Body(grades=grades)


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
    
    stmt = _insert(m.Grade).values(company_id=at.company_id, **body.dict()).returning(m.Grade.id)
    grade_id = await session.scalar(stmt)
    return sch.Create.Response.Body(id=grade_id)


@router.delete('/{id}',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError
                   ),
               response_model=sch.Delete.Response.Body
               )
async def delete(id: UUID,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = _delete(m.Grade) \
           .where(m.Grade.id == id) \
           .where(m.Grade.company_id == at.company_id) \
           .returning(m.Grade.id)
           
    try:
        grade_id = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.Delete.Response.Body(id=grade_id)

