#!/usr/bin/env python3
"""
Employee Hours Tool for OpenClaw Voice Vision
Query timesheet data and employee information
"""

import sys
import os

# Handle both direct execution and module import
try:
    from mock_data import MOCK_EMPLOYEES
    from mock_databricks import MockDatabricksClient
except ImportError:
    from scripts.mock_data import MOCK_EMPLOYEES
    from scripts.mock_databricks import MockDatabricksClient
from typing import Dict, Any, Optional

class EmployeeHours:
    """Query employee data"""
    
    def __init__(self, client=None):
        self.client = client or MockDatabricksClient()
        self.table = os.getenv('EMPLOYEES_TABLE', 'employees')
    
    def get_employee_hours(self, employee_id: str, date_range: str = "this week") -> Dict[str, Any]:
        """Get hours for a specific employee"""
        
        # Search mock data
        for emp in MOCK_EMPLOYEES:
            if emp["employee_id"].upper() == employee_id.upper() or \
               emp["name"].lower().startswith(employee_id.lower()):
                return {
                    "found": True,
                    "employee_id": emp["employee_id"],
                    "name": emp["name"],
                    "department": emp["department"],
                    "shift": emp["shift"],
                    "hours_this_week": emp["hours_this_week"],
                    "hours_last_week": emp["hours_last_week"],
                    "status": emp["status"],
                    "date_range": date_range
                }
        
        return {
            "found": False,
            "message": f"Employee {employee_id} not found",
            "employee_id": employee_id
        }
    
    def get_department_roster(self, department: str, shift: Optional[str] = None) -> Dict[str, Any]:
        """Get employees in a department"""
        
        employees = [e for e in MOCK_EMPLOYEES 
                    if e["department"].lower() == department.lower()]
        
        if shift:
            employees = [e for e in employees if e["shift"].lower() == shift.lower()]
        
        return {
            "found": len(employees) > 0,
            "department": department,
            "shift": shift,
            "count": len(employees),
            "employees": employees
        }
    
    def search_employees(self, query: str) -> Dict[str, Any]:
        """Search employees by name or ID"""
        
        matches = []
        for emp in MOCK_EMPLOYEES:
            if (query.lower() in emp["name"].lower() or 
                query.lower() in emp["employee_id"].lower()):
                matches.append(emp)
        
        return {
            "found": len(matches) > 0,
            "query": query,
            "count": len(matches),
            "employees": matches
        }
    
    def format_hours_response(self, data: Dict[str, Any]) -> str:
        """Format as natural language"""
        if not data.get("found"):
            return data.get("message", f"Sorry, I couldn't find that employee")
        
        name = data.get("name")
        hours = data.get("hours_this_week", 0)
        department = data.get("department")
        status = data.get("status")
        
        response = f"{name} from {department}. "
        response += f"{hours} hours logged this week. "
        
        if status != "Active":
            response += f"Status: {status}. "
        
        # Compare to last week
        last_week = data.get("hours_last_week", 0)
        if last_week > 0:
            diff = hours - last_week
            if abs(diff) > 5:
                direction = "up" if diff > 0 else "down"
                response += f"That's {abs(diff):.1f} hours {direction} from last week. "
        
        return response
    
    def format_roster_response(self, data: Dict[str, Any]) -> str:
        """Format department roster"""
        if not data.get("found"):
            return f"No employees found in {data.get('department')}"
        
        dept = data.get("department")
        shift = data.get("shift")
        count = data.get("count", 0)
        employees = data.get("employees", [])
        
        shift_text = f" {shift} shift" if shift else ""
        response = f"{count} employees in{shift_text} {dept}: "
        
        names = [e["name"].split()[0] for e in employees[:5]]
        response += ", ".join(names)
        
        if count > 5:
            response += f", and {count - 5} more"
        
        return response


def main():
    """CLI demo"""
    print("👤 Employee Hours Demo")
    print("=" * 50)
    
    eh = EmployeeHours()
    
    # Test 1: Get employee hours
    print("\n1. Get hours for John...")
    result = eh.get_employee_hours("John")
    print(f"   {eh.format_hours_response(result)}")
    
    # Test 2: Department roster
    print("\n2. Assembly department roster...")
    result = eh.get_department_roster("Assembly")
    print(f"   {eh.format_roster_response(result)}")
    
    # Test 3: Night shift
    print("\n3. Night shift employees...")
    result = eh.get_department_roster("Assembly", shift="Night")
    print(f"   {eh.format_roster_response(result)}")
    
    # Test 4: Search
    print("\n4. Search for 'Sarah'...")
    result = eh.search_employees("Sarah")
    if result["found"]:
        for emp in result["employees"]:
            print(f"   - {emp['name']} ({emp['department']})")

if __name__ == "__main__":
    main()
