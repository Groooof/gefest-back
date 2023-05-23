from uuid import UUID
from datetime import datetime

import pydantic as pd


class RefreshToken:
    class Create:
        class Input(pd.BaseModel):
            user_id: UUID
            token: UUID
            expires_at: datetime
            
    class Update:
        class Input(pd.BaseModel):
            token: UUID
            new_token: UUID
            new_expires_at: datetime
            
    class Delete:
        class Input(pd.BaseModel):
            token: UUID
            
    class Verify:
        class Input(pd.BaseModel):
            user_id: UUID
            token: UUID
        




