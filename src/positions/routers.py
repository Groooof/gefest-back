from uuid import UUID
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import exc as sa_exc

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

from ..service.pd_models import position


router = APIRouter(tags=['positions'], prefix='/positions')


@router.get('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetCompanyPositions.Response.Body
             )
async def get_company_positions(session: AsyncSession = Depends(get_session),
                                at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = select(m.User.company_id).where(m.User.id == at.user_id)
    res = await session.scalars(stmt)
    company_id = res.one()
    
    res = await session.scalars(select(m.Position).where(m.Position.company_id == company_id))
    return sch.GetCompanyPositions.Response.Body(
        departments=[position.Read.from_orm(orm_model) for orm_model in res.all()]
    )


@router.post('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.CreateCompanyPosition.Response.Body
             )
async def create_company_position(body: sch.CreateCompanyPosition.Request.Body,
                                  session: AsyncSession = Depends(get_session),
                                  at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = insert(m.Position).values(company_id=at.company_id, **body.dict()).returning(m.Position.id)
    res = await session.execute(stmt)
    return sch.CreateCompanyPosition.Response.Body(id=res.scalars().one())


@router.delete('/{id}',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError
                   ),
               response_model=sch.DeleteCompanyPosition.Response.Body
               )
async def delete_company_position(id: UUID,
                                  session: AsyncSession = Depends(get_session),
                                  at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = delete(m.Position).where(
        (m.Position.id == id) 
        &
        (m.Position.company_id == at.company_id)
    ).returning(m.Position.id)
    res = await session.execute(stmt)
    try:
        position_id = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    return sch.DeleteCompanyPosition.Response.Body(id=position_id)

