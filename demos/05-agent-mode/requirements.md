# Employee Directory API — Requirements

## Overview
Build a simple Employee Directory REST API for a small company.

### Data Model — Employee
| Field        | Type     | Constraints                          |
|-------------|----------|--------------------------------------|
| id          | integer  | Auto-generated primary key           |
| first_name  | string   | Required, 1-50 characters            |
| last_name   | string   | Required, 1-50 characters            |
| email       | string   | Required, valid email, unique         |
| department  | string   | Required, from predefined list        |
| title       | string   | Required                             |
| hire_date   | date     | Required, cannot be in the future    |
| salary      | float    | Required, must be positive            |
| is_active   | boolean  | Defaults to true                     |

### Valid Departments
Engineering, Marketing, Sales, Human Resources, Finance, Operations

### API Endpoints

1. **POST /employees** — Create a new employee
2. **GET /employees** — List all employees (with optional filters: department, is_active)
3. **GET /employees/{id}** — Get a single employee by ID
4. **PUT /employees/{id}** — Update an employee
5. **DELETE /employees/{id}** — Soft-delete (set is_active=false)
6. **GET /employees/stats** — Return department-level statistics:
   - Count of active employees per department
   - Average salary per department

### Non-functional Requirements
- Return proper HTTP status codes (201, 200, 404, 422)
- Input validation with meaningful error messages
- Include a health check endpoint: GET /health
