from pydantic import BaseModel


class APIName(BaseModel):
    trap_name: str

class APINameChange(BaseModel):
    old: str
    new: str

class APITrap(BaseModel):
    trap_name: str
    open: bool
