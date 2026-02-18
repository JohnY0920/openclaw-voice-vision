#!/usr/bin/env python3
"""
Mock Databricks Client for Testing
Use this when you don't have real credentials yet
"""

from typing import Dict, Any, Optional
from mock_data import MOCK_INVENTORY, MOCK_PRODUCTION_JOBS, MOCK_EMPLOYEES, MOCK_CUSTOMERS

class MockDatabricksClient:
    """Mock client that returns sample data for testing"""
    
    def __init__(self):
        print("🎭 Using MOCK Databricks client (no real credentials needed)")
    
    def execute_statement(self, sql: str, **kwargs) -> Dict[str, Any]:
        """Mock SQL execution - parses simple queries and returns mock data"""
        
        sql_lower = sql.lower()
        
        # Inventory queries
        if "inventory" in sql_lower or "sku" in sql_lower:
            return self._handle_inventory_query(sql_lower)
        
        # Production queries
        if "production" in sql_lower or "job" in sql_lower:
            return self._handle_production_query(sql_lower)
        
        # Employee queries
        if "employee" in sql_lower:
            return self._handle_employee_query(sql_lower)
        
        # Customer queries
        if "customer" in sql_lower:
            return self._handle_customer_query(sql_lower)
        
        # Default: return mock success
        return {
            "status": {"state": "SUCCEEDED"},
            "result": {
                "data_array": [["Mock data - query not recognized", sql]],
                "manifest": {"schema": {"columns": [{"name": "message"}, {"name": "query"}]}}
            }
        }
    
    def _handle_inventory_query(self, sql: str) -> Dict[str, Any]:
        """Handle inventory-related queries"""
        
        # Check for specific SKU
        for item in MOCK_INVENTORY:
            if item["sku"].lower() in sql or item["barcode"] in sql:
                return self._format_success([[
                    item["sku"],
                    item["description"],
                    item["quantity_on_hand"],
                    item["quantity_reserved"],
                    item["quantity_available"],
                    item["warehouse_location"],
                    "2026-02-18",
                    item["reorder_point"],
                    item["unit_cost"]
                ]])
        
        # Check for low stock
        if "low" in sql or "reorder" in sql:
            low_stock = [i for i in MOCK_INVENTORY if i["quantity_available"] <= i["reorder_point"]]
            data = [[
                i["sku"],
                i["description"],
                i["quantity_available"],
                i["reorder_point"],
                i["warehouse_location"]
            ] for i in low_stock]
            return self._format_success(data)
        
        # Return all inventory
        data = [[
            i["sku"],
            i["description"],
            i["quantity_available"],
            i["warehouse_location"]
        ] for i in MOCK_INVENTORY]
        return self._format_success(data)
    
    def _handle_production_query(self, sql: str) -> Dict[str, Any]:
        """Handle production job queries"""
        
        # Check for specific job
        for job in MOCK_PRODUCTION_JOBS:
            if job["job_id"].lower() in sql:
                return self._format_success([[
                    job["job_id"],
                    job["customer_name"],
                    job["product_description"],
                    job["quantity_ordered"],
                    job["quantity_produced"],
                    job["quantity_remaining"],
                    job["status"],
                    job["start_date"],
                    job.get("estimated_completion", job.get("actual_completion", "")),
                    job["priority"],
                    job["assigned_work_center"]
                ]])
        
        # Check for customer
        for job in MOCK_PRODUCTION_JOBS:
            if job["customer_name"].lower().split()[0] in sql.lower():
                return self._format_success([[
                    job["job_id"],
                    job["customer_name"],
                    job["product_description"],
                    job["quantity_ordered"],
                    job["quantity_produced"],
                    job["status"],
                    job.get("estimated_completion", job.get("actual_completion", ""))
                ]])
        
        # Return all jobs
        data = [[
            j["job_id"],
            j["customer_name"],
            j["status"],
            j["quantity_produced"],
            j["quantity_ordered"]
        ] for j in MOCK_PRODUCTION_JOBS]
        return self._format_success(data)
    
    def _handle_employee_query(self, sql: str) -> Dict[str, Any]:
        """Handle employee queries"""
        
        # Check for specific employee
        for emp in MOCK_EMPLOYEES:
            if emp["employee_id"].lower() in sql or emp["name"].lower().split()[0] in sql.lower():
                return self._format_success([[
                    emp["employee_id"],
                    emp["name"],
                    emp["department"],
                    emp["shift"],
                    emp["hours_this_week"],
                    emp["status"]
                ]])
        
        # Return all employees
        data = [[
            e["employee_id"],
            e["name"],
            e["department"],
            e["hours_this_week"]
        ] for e in MOCK_EMPLOYEES]
        return self._format_success(data)
    
    def _handle_customer_query(self, sql: str) -> Dict[str, Any]:
        """Handle customer queries"""
        
        # Return all customers
        data = [[
            c["customer_id"],
            c["name"],
            c["contact"],
            c["ytd_revenue"],
            c["outstanding_orders"]
        ] for c in MOCK_CUSTOMERS]
        return self._format_success(data)
    
    def _format_success(self, data_array: list) -> Dict[str, Any]:
        """Format successful response"""
        return {
            "status": {"state": "SUCCEEDED"},
            "result": {
                "data_array": data_array,
                "manifest": {"schema": {"columns": [{"name": f"col_{i}"} for i in range(len(data_array[0]) if data_array else 1)]}}
            }
        }


# Drop-in replacement for real client
try:
    from databricks_query import DatabricksClient
except ImportError:
    DatabricksClient = MockDatabricksClient

if __name__ == "__main__":
    # Test mock client
    client = MockDatabricksClient()
    
    print("\n🧪 Testing Mock Client:")
    print("-" * 50)
    
    # Test inventory lookup
    result = client.execute_statement("SELECT * FROM inventory WHERE sku = 'ABC123'")
    print(f"✅ Inventory query: {result['status']['state']}")
    
    # Test production
    result = client.execute_statement("SELECT * FROM production WHERE job_id = 'JOB001'")
    print(f"✅ Production query: {result['status']['state']}")
    
    # Test employees
    result = client.execute_statement("SELECT * FROM employees")
    print(f"✅ Employee query: {result['status']['state']}")
    
    print("\n🎭 Mock client ready for testing!")
