from uuid import UUID
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.dialects.postgresql import insert as _insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import exc as sa_exc
from sqlalchemy.future import select as _select
from sqlalchemy import delete as _delete

from ..service.fastapi_custom import generate_openapi_responses
from ..service.pd_models import department
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


router = APIRouter(tags=['departments'], prefix='/departments')


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
    
    stmt = _select(m.Department).where(m.Department.company_id == at.company_id)
    res = await session.scalars(stmt)
    departments = [department.Read.from_orm(orm_model) for orm_model in res.all()]
    return sch.GetList.Response.Body(departments=departments)


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
    
    stmt = _insert(m.Department).values(company_id=at.company_id, **body.dict()).returning(m.Department.id)
    department_id = await session.scalar(stmt)
    return sch.Create.Response.Body(id=department_id)


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
    
    stmt = _delete(m.Department) \
          .where(m.Department.id == id) \
          .where(m.Department.company_id == at.company_id) \
          .returning(m.Department.id)
    
    try:
        department_id = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError

    return sch.Delete.Response.Body(id=department_id)
