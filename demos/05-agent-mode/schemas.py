from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from models import VALID_DEPARTMENTS


class EmployeeCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    department: str
    title: str = Field(..., min_length=1)
    hire_date: date
    salary: float = Field(..., gt=0)
    is_active: bool = True

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: str) -> str:
        if v not in VALID_DEPARTMENTS:
            raise ValueError(
                f"Invalid department. Must be one of: {', '.join(VALID_DEPARTMENTS)}"
            )
        return v

    @field_validator("hire_date")
    @classmethod
    def validate_hire_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Hire date cannot be in the future")
        return v


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1)
    hire_date: Optional[date] = None
    salary: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_DEPARTMENTS:
            raise ValueError(
                f"Invalid department. Must be one of: {', '.join(VALID_DEPARTMENTS)}"
            )
        return v

    @field_validator("hire_date")
    @classmethod
    def validate_hire_date(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v > date.today():
            raise ValueError("Hire date cannot be in the future")
        return v


class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    title: str
    hire_date: date
    salary: float
    is_active: bool

    model_config = {"from_attributes": True}


class DepartmentStats(BaseModel):
    department: str
    active_employee_count: int
    average_salary: float
