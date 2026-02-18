#!/usr/bin/env python3
"""
Customer Insights Tool for OpenClaw Voice Vision
Query customer data and order history
"""

import sys
import os

# Handle both direct execution and module import
try:
    from mock_data import MOCK_CUSTOMERS, MOCK_PRODUCTION_JOBS
except ImportError:
    from scripts.mock_data import MOCK_CUSTOMERS, MOCK_PRODUCTION_JOBS
from typing import Dict, Any, List

class CustomerInsights:
    """Query customer information"""
    
    def get_customer_summary(self, customer_name: str) -> Dict[str, Any]:
        """Get full customer profile"""
        
        # Find customer
        customer = None
        for c in MOCK_CUSTOMERS:
            if customer_name.lower() in c["name"].lower():
                customer = c
                break
        
        if not customer:
            return {
                "found": False,
                "message": f"Customer '{customer_name}' not found"
            }
        
        # Get their orders
        orders = [j for j in MOCK_PRODUCTION_JOBS 
                 if j["customer_name"] == customer["name"]]
        
        return {
            "found": True,
            "customer_id": customer["customer_id"],
            "name": customer["name"],
            "contact": customer["contact"],
            "email": customer["email"],
            "phone": customer["phone"],
            "total_orders": customer["total_orders"],
            "ytd_revenue": customer["ytd_revenue"],
            "outstanding_orders": customer["outstanding_orders"],
            "last_contact": customer["last_contact"],
            "orders": orders
        }
    
    def get_order_status(self, customer_name: str) -> Dict[str, Any]:
        """Get order status for a customer"""
        
        customer_data = self.get_customer_summary(customer_name)
        if not customer_data.get("found"):
            return customer_data
        
        orders = customer_data.get("orders", [])
        
        in_progress = [o for o in orders if o["status"] == "IN_PROGRESS"]
        completed = [o for o in orders if o["status"] == "COMPLETED"]
        delayed = [o for o in orders if o["status"] == "DELAYED"]
        
        return {
            "found": True,
            "customer": customer_data["name"],
            "total_orders": len(orders),
            "in_progress": len(in_progress),
            "completed_recent": len(completed),
            "delayed": len(delayed),
            "orders": orders
        }
    
    def get_top_customers(self, limit: int = 5) -> List[Dict]:
        """Get top customers by revenue"""
        sorted_customers = sorted(
            MOCK_CUSTOMERS, 
            key=lambda x: x["ytd_revenue"], 
            reverse=True
        )
        return sorted_customers[:limit]
    
    def format_customer_response(self, data: Dict[str, Any]) -> str:
        """Format customer summary as natural language"""
        if not data.get("found"):
            return data.get("message", "Customer not found")
        
        name = data.get("name")
        revenue = data.get("ytd_revenue", 0)
        orders = data.get("total_orders", 0)
        outstanding = data.get("outstanding_orders", 0)
        contact = data.get("contact")
        
        response = f"{name}. Contact: {contact}. "
        response += f"YTD revenue: ${revenue:,.0f}. "
        response += f"{orders} total orders. "
        
        if outstanding > 0:
            response += f"{outstanding} orders in progress. "
        
        # Last contact
        last_contact = data.get("last_contact")
        if last_contact:
            response += f"Last contact: {last_contact}. "
        
        return response
    
    def format_order_status_response(self, data: Dict[str, Any]) -> str:
        """Format order status as natural language"""
        if not data.get("found"):
            return data.get("message", "Customer not found")
        
        customer = data.get("customer")
        total = data.get("total_orders", 0)
        in_progress = data.get("in_progress", 0)
        delayed = data.get("delayed", 0)
        
        response = f"{customer} has {total} orders. "
        
        if in_progress > 0:
            response += f"{in_progress} in progress. "
        
        if delayed > 0:
            response += f"⚠️ {delayed} delayed. "
        
        # Detail recent orders
        orders = data.get("orders", [])
        if orders:
            recent = [o for o in orders if o["status"] in ["IN_PROGRESS", "DELAYED"]][:2]
            if recent:
                response += "Recent: "
                for o in recent:
                    response += f"{o['job_id']} ({o['status'].lower()}), "
                response = response.rstrip(", ") + ". "
        
        return response


def main():
    """CLI demo"""
    print("👤 Customer Insights Demo")
    print("=" * 50)
    
    ci = CustomerInsights()
    
    # Test 1: Customer summary
    print("\n1. Acme Bicycle Co summary...")
    result = ci.get_customer_summary("Acme")
    print(f"   {ci.format_customer_response(result)}")
    
    # Test 2: Order status
    print("\n2. Order status for City Cycles...")
    result = ci.get_order_status("City")
    print(f"   {ci.format_order_status_response(result)}")
    
    # Test 3: Top customers
    print("\n3. Top customers by revenue...")
    top = ci.get_top_customers(3)
    for i, c in enumerate(top, 1):
        print(f"   {i}. {c['name']}: ${c['ytd_revenue']:,.0f}")

if __name__ == "__main__":
    main()
