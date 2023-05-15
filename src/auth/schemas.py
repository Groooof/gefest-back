import pydantic as pd

    
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
    