from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import Employee, VALID_DEPARTMENTS
from schemas import (
    DepartmentStats,
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(Employee).filter(Employee.email == employee.email).first()
    if existing:
        raise HTTPException(
            status_code=422, detail="An employee with this email already exists"
        )

    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/stats", response_model=list[DepartmentStats])
def get_stats(db: Session = Depends(get_db)):
    results = (
        db.query(
            Employee.department,
            func.count(Employee.id).label("active_employee_count"),
            func.avg(Employee.salary).label("average_salary"),
        )
        .filter(Employee.is_active == True)
        .group_by(Employee.department)
        .all()
    )
    return [
        DepartmentStats(
            department=row.department,
            active_employee_count=row.active_employee_count,
            average_salary=round(row.average_salary, 2),
        )
        for row in results
    ]


@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    department: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Employee)
    if department is not None:
        if department not in VALID_DEPARTMENTS:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid department. Must be one of: {', '.join(VALID_DEPARTMENTS)}",
            )
        query = query.filter(Employee.department == department)
    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)
    return query.all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, updates: EmployeeUpdate, db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = updates.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = (
            db.query(Employee)
            .filter(Employee.email == update_data["email"], Employee.id != employee_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=422, detail="An employee with this email already exists"
            )

    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", response_model=EmployeeResponse)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.is_active = False
    db.commit()
    db.refresh(employee)
    return employee
