from typing import Optional
from pydantic import BaseModel

class ApiResponse(BaseModel):
    # code: int
    # success: bool
    data: list = []
    
class ApiObjectResponse(BaseModel):
    # code: int
    # success: bool
    data: dict

class PollingStationCreate(BaseModel):
    stamp: int
    results: dict
    participant_id: int
    polling_station_id: int
    constituency_id: Optional[int]
    polling_station_name: Optional[str]

class ParliamentaryResultsCreate(BaseModel):
    stamp: int
    results: dict
    participant_id: int
    constituency_id: int

class PresidentialResultsCreate(BaseModel):
    stamp: int
    results: dict
    participant_id: int
    constituency_id: int

class ConstituencyWinnerCreate(BaseModel):
    candidate_id: int
    constituency_id: int

class IncidentCreate(BaseModel):
    participant_id: int
    constituency_id: int
    polling_station_id: int
    report: list
    stamp: int
    description: Optional[str]

class UpdateReporter(BaseModel):
    rec_id: str
    phone_number: str
    gender: str 
    constituency_id: int 
    name: str


class UpdateParliamentary(BaseModel):
    rec_id: int
    constituency_id: int 
