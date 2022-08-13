from pydantic import BaseModel
from typing import Optional


class Company(BaseModel):
    id: Optional[int] = None
    company_name: str
    founder: str
    year_established: str
    current_networth :str
    hq: str
    country: str 