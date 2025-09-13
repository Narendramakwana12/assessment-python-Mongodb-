from fastapi import APIRouter, HTTPException, Query, Body
from database import employees_collection
from models import Employee, EmployeeUpdate

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Employee API with MongoDB is running 🚀"}

from datetime import date, datetime

@router.post("/employees")
def create_employee(employee: Employee):
    existing = employees_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    emp_dict = employee.dict()

    
    if isinstance(emp_dict["joining_date"], date):
        emp_dict["joining_date"] = datetime.combine(emp_dict["joining_date"], datetime.min.time())

    employees_collection.insert_one(emp_dict)
    return {"message": "Employee added successfully!"}


@router.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: str):
    employee = employees_collection.find_one({"employee_id": employee_id}, {"_id": 0})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/employees/{employee_id}")
def update_employee(employee_id: str, updated_data: EmployeeUpdate = Body(...)):
    update_dict = {k: v for k, v in updated_data.dict().items() if v is not None}
    result = employees_collection.update_one(
        {"employee_id": employee_id}, {"$set": update_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    result = employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}


@router.get("/employees")
def list_employees(department: str = Query(None)):
    query = {}
    if department:
        query["department"] = department

    employees = list(
        employees_collection.find(query, {"_id": 0}).sort("joining_date", -1)
    )
    return {"employees": employees}


@router.get("/employees/avg-salary")
def avg_salary_by_department():
    employees = list(employees_collection.find({}, {"_id": 0, "department": 1, "salary": 1}))
    if not employees:
        return {"message": "No employees found"}

    dept_salary = {}
    dept_count = {}
    for emp in employees:
        dept = emp.get("department")
        salary = emp.get("salary", 0)
        if dept:
            dept_salary[dept] = dept_salary.get(dept, 0) + salary
            dept_count[dept] = dept_count.get(dept, 0) + 1

  
    avg_salary_list = [
        {"department": dept, "avg_salary": round(dept_salary[dept] / dept_count[dept], 2)}
        for dept in dept_salary
    ]

    return {"avg_salary_by_department": avg_salary_list}


@router.get("/employees/search")
def search_employees(skill: str):
    employees = list(
        employees_collection.find({"skills": {"$in": [skill]}}, {"_id": 0})
    )
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found with this skill")
    return {"employees": employees}
