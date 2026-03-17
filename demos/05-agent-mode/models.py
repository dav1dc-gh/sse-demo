from sqlalchemy import Column, Integer, String, Float, Boolean, Date, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

VALID_DEPARTMENTS = [
    "Engineering",
    "Marketing",
    "Sales",
    "Human Resources",
    "Finance",
    "Operations",
]


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    department = Column(String, nullable=False)
    title = Column(String, nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
