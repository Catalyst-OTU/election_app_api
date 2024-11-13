from pydantic import BaseModel, Field
from typing import Optional

import datetime

class UserBase(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str

class Reporter(BaseModel):
    reporter_name: str
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str
    gender: str
    constituency_id: int