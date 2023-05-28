import pydantic as pd
from uuid import UUID

    
class Login:
    class Request:
        class Body(pd.BaseModel):
            username: str
            password: str

            class Config:
                schema_extra = {
                    "title": "LoginRequestBody",
                    "example": {
                        "username": "admin",
                        "password": "admin"
                    }
                }
                
    class Response:
        class Body(pd.BaseModel):
            user_id: UUID
            role_code: int
    