from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: float
    joining_date: date
    skills: List[str]

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None
