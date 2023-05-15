import pydantic as pd


class Error(pd.BaseModel):
    error: str
    error_description: str
