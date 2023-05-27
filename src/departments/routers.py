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

from ..service.pd_models import department


router = APIRouter(tags=['departments'], prefix='/departments')


@router.get('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetCompanyDepartments.Response.Body
             )
async def get_company_departments(session: AsyncSession = Depends(get_session),
                                  at: AccessToken = Depends(AccessJWTCookie())):
        
    res = await session.scalars(select(m.Department).where(m.Department.company_id == at.company_id))
    return sch.GetCompanyDepartments.Response.Body(
        departments=[department.Read.from_orm(orm_model) for orm_model in res.all()]
    )


@router.post('',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.CreateCompanyDepartment.Response.Body
             )
async def create_company_department(body: sch.CreateCompanyDepartment.Request.Body,
                                    session: AsyncSession = Depends(get_session),
                                    at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = insert(m.Department).values(company_id=at.company_id, **body.dict()).returning(m.Department.id)
    res = await session.execute(stmt)
    return sch.CreateCompanyDepartment.Response.Body(id=res.scalars().one())


@router.delete('/{id}',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError
                   ),
               response_model=sch.DeleteCompanyDepartment.Response.Body
               )
async def delete_company_department(id: UUID,
                                    session: AsyncSession = Depends(get_session),
                                    at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = delete(m.Department).where(
        (m.Department.id == id) 
        &
        (m.Department.company_id == at.company_id)
    ).returning(m.Department.id)
    res = await session.execute(stmt)
    try:
        department_id = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    return sch.DeleteCompanyDepartment.Response.Body(id=department_id)

