from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel, Field


class Read(BaseModel):
    id: UUID
    name: str
    
    class Config:
        orm_mode = True
    
    
class Create(BaseModel):
    name: str
    
    
class Update(BaseModel):
    name: str
