from pydantic import BaseModel
from typing import Optional, List, Dict

class FacultyOut(BaseModel):
    id: int
    faculty_type: Optional[str]
    name: Optional[str]
    education: Optional[str]
    address: Optional[str]
    specializations: Optional[str]
    biography: Optional[str]
    research: Optional[str]

    phone: Optional[Dict[str, List[str]]]
    email: Optional[List[str]]
    teaching: Optional[List[str]]
    publications: Optional[List[str]]
    website_links: Optional[Dict[str, List[str]]]

    class Config:
        orm_mode = True
