
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="My First Render API")


# Temporary in-memory database
employees = []


class Employee(BaseModel):
    name: str
    role: str
    salary: int


@app.get("/")
def home():
    return {"message": "FastAPI is running on Render!"}


# CREATE
@app.post("/employees")
def create_employee(employee: Employee):
    data = employee.model_dump()
    data["id"] = len(employees) + 1
    employees.append(data)

    return {"message": "Employee created", "data": data}


# READ
@app.get("/employees")
def get_employees():
    return employees


# READ BY ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


# UPDATE
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated: Employee):
    for employee in employees:
        if employee["id"] == employee_id:
            employee.update(updated.model_dump())
            return {"message": "Employee updated", "data": employee}

    raise HTTPException(status_code=404, detail="Employee not found")


# DELETE
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            employees.remove(employee)
            return {"message": "Employee deleted"}

    raise HTTPException(status_code=404, detail="Employee not found")
