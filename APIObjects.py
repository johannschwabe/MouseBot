from pydantic import BaseModel


class APIId(BaseModel):
    trap_id: str


class APITrap(BaseModel):
    trap_id: str
    trap_name: str
    open: bool
