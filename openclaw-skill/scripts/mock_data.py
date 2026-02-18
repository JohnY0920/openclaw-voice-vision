# Mock Data for Testing
# Use this when you don't have real Databricks credentials yet

MOCK_INVENTORY = [
    {
        "sku": "ABC123",
        "description": "Red Bicycle Helmet",
        "barcode": "123456789012",
        "quantity_on_hand": 450,
        "quantity_reserved": 50,
        "quantity_available": 400,
        "warehouse_location": "A-12-3",
        "unit_cost": 25.50,
        "reorder_point": 100
    },
    {
        "sku": "DEF456",
        "description": "Mountain Bike Frame - Carbon",
        "barcode": "987654321098",
        "quantity_on_hand": 25,
        "quantity_reserved": 5,
        "quantity_available": 20,
        "warehouse_location": "B-05-1",
        "unit_cost": 450.00,
        "reorder_point": 10
    },
    {
        "sku": "XYZ789",
        "description": "Hydraulic Brake Set",
        "barcode": "555666777888",
        "quantity_on_hand": 120,
        "quantity_reserved": 30,
        "quantity_available": 90,
        "warehouse_location": "C-08-4",
        "unit_cost": 85.00,
        "reorder_point": 50
    },
    {
        "sku": "LOW001",
        "description": "Titanium Seat Post",
        "barcode": "111222333444",
        "quantity_on_hand": 8,
        "quantity_reserved": 2,
        "quantity_available": 6,
        "warehouse_location": "A-03-2",
        "unit_cost": 120.00,
        "reorder_point": 15  # Below reorder point
    }
]

MOCK_PRODUCTION_JOBS = [
    {
        "job_id": "JOB001",
        "customer_name": "Acme Bicycle Co",
        "product_description": "50x Custom Road Bikes - Red",
        "quantity_ordered": 50,
        "quantity_produced": 40,
        "quantity_remaining": 10,
        "status": "IN_PROGRESS",
        "start_date": "2026-02-10",
        "estimated_completion": "2026-02-20",
        "priority": "HIGH",
        "assigned_work_center": "Assembly Line 1"
    },
    {
        "job_id": "JOB002",
        "customer_name": "Mountain Adventures",
        "product_description": "25x MTB Frames - Carbon",
        "quantity_ordered": 25,
        "quantity_produced": 25,
        "quantity_remaining": 0,
        "status": "COMPLETED",
        "start_date": "2026-02-01",
        "actual_completion": "2026-02-15",
        "priority": "NORMAL",
        "assigned_work_center": "Carbon Fiber Shop"
    },
    {
        "job_id": "JOB003",
        "customer_name": "City Cycles",
        "product_description": "100x Urban Commuter Bikes",
        "quantity_ordered": 100,
        "quantity_produced": 15,
        "quantity_remaining": 85,
        "status": "IN_PROGRESS",
        "start_date": "2026-02-12",
        "estimated_completion": "2026-03-01",
        "priority": "NORMAL",
        "assigned_work_center": "Assembly Line 2"
    },
    {
        "job_id": "JOB004",
        "customer_name": "Racing Team Pro",
        "product_description": "10x Pro Racing Frames",
        "quantity_ordered": 10,
        "quantity_produced": 0,
        "quantity_remaining": 10,
        "status": "DELAYED",
        "start_date": "2026-02-05",
        "estimated_completion": "2026-02-10",  # Overdue
        "priority": "URGENT",
        "assigned_work_center": "Prototype Shop"
    }
]

MOCK_EMPLOYEES = [
    {
        "employee_id": "EMP001",
        "name": "John Smith",
        "department": "Assembly",
        "shift": "Day",
        "hours_this_week": 38.5,
        "hours_last_week": 42.0,
        "status": "Active"
    },
    {
        "employee_id": "EMP002",
        "name": "Sarah Johnson",
        "department": "Quality Control",
        "shift": "Day",
        "hours_this_week": 40.0,
        "hours_last_week": 38.0,
        "status": "Active"
    },
    {
        "employee_id": "EMP003",
        "name": "Mike Chen",
        "department": "Assembly",
        "shift": "Night",
        "hours_this_week": 36.0,
        "hours_last_week": 40.0,
        "status": "Active"
    },
    {
        "employee_id": "EMP004",
        "name": "Lisa Rodriguez",
        "department": "Shipping",
        "shift": "Night",
        "hours_this_week": 32.0,
        "hours_last_week": 35.0,
        "status": "On Leave"
    }
]

MOCK_CUSTOMERS = [
    {
        "customer_id": "CUST001",
        "name": "Acme Bicycle Co",
        "contact": "John Buyer",
        "email": "john@acmebikes.com",
        "phone": "555-0101",
        "total_orders": 12,
        "ytd_revenue": 125000.00,
        "outstanding_orders": 2,
        "last_contact": "2026-02-16"
    },
    {
        "customer_id": "CUST002",
        "name": "Mountain Adventures",
        "contact": "Sarah Manager",
        "email": "sarah@mtnadventures.com",
        "phone": "555-0202",
        "total_orders": 8,
        "ytd_revenue": 89000.00,
        "outstanding_orders": 1,
        "last_contact": "2026-02-14"
    },
    {
        "customer_id": "CUST003",
        "name": "City Cycles",
        "contact": "Mike Owner",
        "email": "mike@citycycles.com",
        "phone": "555-0303",
        "total_orders": 25,
        "ytd_revenue": 320000.00,
        "outstanding_orders": 3,
        "last_contact": "2026-02-17"
    }
]
