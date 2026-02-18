#!/usr/bin/env python3
"""
Complete System Demo - All Tools
Demonstrates the full OpenClaw Voice Vision system
"""

import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from mock_data import MOCK_INVENTORY, MOCK_PRODUCTION_JOBS, MOCK_EMPLOYEES, MOCK_CUSTOMERS
from mock_databricks import MockDatabricksClient

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print('='*60)

def demo_inventory():
    """Inventory management demo"""
    print_header("INVENTORY MANAGEMENT")
    
    print("\n📦 Scenario: Worker scans barcode '123456789012'")
    print("👤 Voice: 'What am I looking at?'")
    
    # Find item
    barcode = "123456789012"
    item = next((i for i in MOCK_INVENTORY if i["barcode"] == barcode), None)
    
    if item:
        print(f"\n🔍 Found: {item['description']}")
        print(f"📋 SKU: {item['sku']}")
        print(f"📦 Available: {item['quantity_available']} units")
        print(f"📍 Location: {item['warehouse_location']}")
        print(f"💰 Unit cost: ${item['unit_cost']:.2f}")
        
        # Voice response
        response = f"{item['description']}, SKU {item['sku']}. {item['quantity_available']} units available at {item['warehouse_location']}."
        if item['quantity_available'] <= item['reorder_point']:
            response += f" Warning: Below reorder point of {item['reorder_point']}."
        print(f"\n🔊 AI Response: \"{response}\"")
    
    # Low stock alert
    print("\n⚠️  Low Stock Items:")
    low_stock = [i for i in MOCK_INVENTORY if i["quantity_available"] <= i["reorder_point"]]
    for item in low_stock:
        print(f"   • {item['sku']}: {item['quantity_available']} units (reorder at {item['reorder_point']})")

def demo_production():
    """Production tracking demo"""
    print_header("PRODUCTION TRACKING")
    
    print("\n🏭 Scenario: Manager asks about job status")
    print("👤 Voice: 'What's the status of job JOB001?'")
    
    job = next((j for j in MOCK_PRODUCTION_JOBS if j["job_id"] == "JOB001"), None)
    
    if job:
        print(f"\n📋 Job: {job['job_id']}")
        print(f"👤 Customer: {job['customer_name']}")
        print(f"📦 Product: {job['product_description']}")
        print(f"📊 Status: {job['status']}")
        print(f"📈 Progress: {job['quantity_produced']}/{job['quantity_ordered']}")
        print(f"🎯 Priority: {job['priority']}")
        print(f"🏭 Work Center: {job['assigned_work_center']}")
        
        # Voice response
        remaining = job['quantity_remaining']
        response = f"Job {job['job_id']} for {job['customer_name']}. {job['product_description']}. Status: {job['status']}. {job['quantity_produced']} of {job['quantity_ordered']} units produced."
        if remaining > 0:
            response += f" {remaining} units remaining."
        print(f"\n🔊 AI Response: \"{response}\"")
    
    # Overdue jobs
    print("\n🚨 Overdue Jobs:")
    overdue = [j for j in MOCK_PRODUCTION_JOBS if j["status"] == "DELAYED"]
    for job in overdue:
        print(f"   • {job['job_id']}: {job['customer_name']} - {job['priority']} priority")

def demo_employees():
    """Employee hours demo"""
    print_header("EMPLOYEE MANAGEMENT")
    
    print("\n👤 Scenario: Supervisor checks employee hours")
    print("👤 Voice: 'How many hours did John work this week?'")
    
    employee = next((e for e in MOCK_EMPLOYEES if "John" in e["name"]), None)
    
    if employee:
        print(f"\n👤 Employee: {employee['name']}")
        print(f"🆔 ID: {employee['employee_id']}")
        print(f"🏢 Department: {employee['department']}")
        print(f"🕐 Shift: {employee['shift']}")
        print(f"⏱️  This Week: {employee['hours_this_week']} hours")
        print(f"⏱️  Last Week: {employee['hours_last_week']} hours")
        print(f"📊 Status: {employee['status']}")
        
        # Voice response
        diff = employee['hours_this_week'] - employee['hours_last_week']
        response = f"{employee['name']} from {employee['department']}. {employee['hours_this_week']} hours logged this week."
        if abs(diff) > 2:
            direction = "up" if diff > 0 else "down"
            response += f" That's {abs(diff):.1f} hours {direction} from last week."
        print(f"\n🔊 AI Response: \"{response}\"")
    
    # Department roster
    print("\n📋 Assembly Department Roster:")
    assembly = [e for e in MOCK_EMPLOYEES if e["department"] == "Assembly"]
    for emp in assembly:
        print(f"   • {emp['name']} ({emp['shift']} shift, {emp['hours_this_week']}h)")

def demo_customers():
    """Customer insights demo"""
    print_header("CUSTOMER INSIGHTS")
    
    print("\n👤 Scenario: Sales checks customer status")
    print("👤 Voice: 'Give me a summary of Acme Bicycle Co'")
    
    customer = next((c for c in MOCK_CUSTOMERS if "Acme" in c["name"]), None)
    
    if customer:
        print(f"\n🏢 Customer: {customer['name']}")
        print(f"👤 Contact: {customer['contact']}")
        print(f"📧 Email: {customer['email']}")
        print(f"📞 Phone: {customer['phone']}")
        print(f"💰 YTD Revenue: ${customer['ytd_revenue']:,.2f}")
        print(f"📦 Total Orders: {customer['total_orders']}")
        print(f"🔄 Outstanding: {customer['outstanding_orders']}")
        print(f"📅 Last Contact: {customer['last_contact']}")
        
        # Get their orders
        orders = [j for j in MOCK_PRODUCTION_JOBS if j["customer_name"] == customer["name"]]
        if orders:
            print(f"\n📋 Active Orders:")
            for order in orders:
                status_emoji = "🟢" if order["status"] == "IN_PROGRESS" else "✅" if order["status"] == "COMPLETED" else "🔴"
                print(f"   {status_emoji} {order['job_id']}: {order['product_description']} ({order['status']})")
        
        # Voice response
        response = f"{customer['name']}. Contact: {customer['contact']}. YTD revenue: ${customer['ytd_revenue']:,.0f}. {customer['total_orders']} total orders. {customer['outstanding_orders']} orders in progress. Last contact: {customer['last_contact']}."
        print(f"\n🔊 AI Response: \"{response}\"")

def demo_full_conversation():
    """Simulate a complete voice interaction"""
    print_header("FULL CONVERSATION DEMO")
    
    print("\n🎭 Scenario: Factory floor worker using Meta glasses")
    print("-" * 60)
    
    conversation = [
        ("👤 Worker", "What am I looking at?"),
        ("🤖 AI", "I see a red bicycle helmet with a barcode label. Would you like me to scan it?"),
        ("👤 Worker", "Yes, scan it."),
        ("🤖 AI", "Red Bicycle Helmet, SKU ABC123. 400 units available at A-12-3."),
        ("👤 Worker", "Where is the carbon fiber frame?"),
        ("🤖 AI", "Let me check... Mountain Bike Frame - Carbon, SKU DEF456. 20 units available at B-05-1."),
        ("👤 Worker", "What's the status of the Acme order?"),
        ("🤖 AI", "Job JOB001 for Acme Bicycle Co. 50x Custom Road Bikes - Red. Status: In Progress. 40 of 50 units produced. 10 units remaining."),
        ("👤 Worker", "Thanks!"),
        ("🤖 AI", "You're welcome! Let me know if you need anything else."),
    ]
    
    for speaker, text in conversation:
        print(f"{speaker}: \"{text}\"")
    
    print("\n✅ Full voice + vision interaction complete!")

def main():
    """Run all demos"""
    print("🔮 OpenClaw Voice Vision - Complete System Demo")
    print("=" * 60)
    print("\nThis demonstrates all capabilities with mock data.")
    print("No hardware or real credentials needed!")
    
    demo_inventory()
    demo_production()
    demo_employees()
    demo_customers()
    demo_full_conversation()
    
    print_header("DEMO COMPLETE")
    print("\n✅ All systems functional!")
    print("\n📊 Summary:")
    print(f"   • {len(MOCK_INVENTORY)} inventory items")
    print(f"   • {len(MOCK_PRODUCTION_JOBS)} production jobs")
    print(f"   • {len(MOCK_EMPLOYEES)} employees")
    print(f"   • {len(MOCK_CUSTOMERS)} customers")
    
    print("\n🚀 Next Steps:")
    print("   1. Get Meta Ray-Ban glasses ($299)")
    print("   2. Get Databricks credentials from client")
    print("   3. Build iOS app in Xcode")
    print("   4. Test with real hardware!")
    
    print("\n📁 Repository:")
    print("   https://github.com/JohnY0920/openclaw-voice-vision")

if __name__ == "__main__":
    main()
