from domains.users.schemas.users import UserBase, Reporter
from pydantic import BaseModel
from typing import Optional

class Auth(UserBase):
    pass
  
class Tokens(BaseModel):
    token: Optional[str]
    refresh_token: str

class Token(BaseModel):
    token: str
