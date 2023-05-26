from pydantic import BaseModel

from . import schemas as sch


class Candidate(sch.Candidate):
    ...


class Candidates:
    class Create:
        class Input(BaseModel):
            ...

