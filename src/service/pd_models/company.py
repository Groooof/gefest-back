from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel, Field


class Read(BaseModel):
    full_name: str
    short_name: str
    ogrn: str
    created_at: datetime
    
    class Config:
        orm_mode = True

