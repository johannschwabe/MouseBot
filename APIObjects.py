from pydantic import BaseModel


class APIName(BaseModel):
    trap_name: str

class APIId(BaseModel):
    trap_id: str

class APINameChange(BaseModel):
    old: str
    new: str

class APITrap(BaseModel):
    trap_id: str
    open: bool
