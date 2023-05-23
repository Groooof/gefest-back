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
            
            class Config:
                schema_extra = {
                    "title": "LoginResponseBody",
                    "example": {
                        "user_id": "fedc2752-e073-4c4f-8f63-42132deea4e3",
                        "role_code": "1"
                    }
                }
    