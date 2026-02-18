#!/usr/bin/env python3
"""
Demo Mode for OpenClaw Voice Vision
Test the full pipeline without Meta glasses or real credentials
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.mock_databricks import MockDatabricksClient
from scripts.mock_data import MOCK_INVENTORY, MOCK_PRODUCTION_JOBS, MOCK_EMPLOYEES

def demo_inventory_lookup():
    """Demo: Look up inventory by SKU"""
    print("\n📦 INVENTORY LOOKUP DEMO")
    print("=" * 50)
    
    client = MockDatabricksClient()
    
    # Test SKU lookup
    print("\n1. Looking up SKU 'ABC123'...")
    result = client.execute_statement("SELECT * FROM inventory WHERE sku = 'ABC123'")
    if result.get('status', {}).get('state') == 'SUCCEEDED':
        data = result.get('result', {}).get('data_array', [])
        if data:
            row = data[0]
            print(f"   ✅ Found: {row[1]}")
            print(f"   📦 Available: {row[4]} units")
            print(f"   📍 Location: {row[5]}")
    
    # Test barcode lookup
    print("\n2. Looking up barcode '987654321098'...")
    result = client.execute_statement("SELECT * FROM inventory WHERE barcode = '987654321098'")
    if result.get('status', {}).get('state') == 'SUCCEEDED':
        data = result.get('result', {}).get('data_array', [])
        if data:
            row = data[0]
            print(f"   ✅ Found: {row[0]}")
            print(f"   📍 Location: {row[5]}")
    
    # Test low stock
    print("\n3. Low stock items:")
    result = client.execute_statement("SELECT * FROM inventory WHERE quantity_available <= reorder_point")
    if result.get('status', {}).get('state') == 'SUCCEEDED':
        data = result.get('result', {}).get('data_array', [])
        for row in data:
            print(f"   ⚠️  {row[0]}: {row[2]} units available")

def demo_production_status():
    """Demo: Check production jobs"""
    print("\n\n🏭 PRODUCTION STATUS DEMO")
    print("=" * 50)
    
    client = MockDatabricksClient()
    
    # Test job lookup
    print("\n1. Checking job 'JOB001'...")
    result = client.execute_statement("SELECT * FROM production WHERE job_id = 'JOB001'")
    if result.get('status', {}).get('state') == 'SUCCEEDED':
        data = result.get('result', {}).get('data_array', [])
        if data:
            row = data[0]
            print(f"   👤 Customer: {row[1]}")
            print(f"   📊 Status: {row[6]}")
            print(f"   📈 Progress: {row[4]}/{row[3]}")
    
    # Test overdue jobs
    print("\n2. Overdue jobs:")
    result = client.execute_statement("SELECT * FROM production WHERE status = 'DELAYED'")
    if result.get('status', {}).get('state') == 'SUCCEEDED':
        data = result.get('result', {}).get('data_array', [])
        for row in data:
            due_date = row[8] if len(row) > 8 else "Unknown"
            print(f"   🚨 {row[0]}: {row[1]} - Due: {due_date}")

def demo_full_pipeline():
    """Demo: Simulate the full voice + vision pipeline"""
    print("\n\n🎭 FULL PIPELINE DEMO")
    print("=" * 50)
    print("\n📱 Simulating: User wearing glasses scans a barcode...")
    print("\n👤 User: 'What am I looking at?'")
    print("🤖 AI: (Processes visual input from camera)")
    print("📷 Camera: Detects barcode '123456789012'")
    print("🔍 Tool Call: inventory_lookup(barcode='123456789012')")
    
    client = MockDatabricksClient()
    result = client.execute_statement("SELECT * FROM inventory WHERE barcode = '123456789012'")
    
    if result.get('status', {}).get('state') == 'SUCCEEDED':
        data = result.get('result', {}).get('data_array', [])
        if data:
            item = data[0]
            print(f"📊 Database: Returns inventory data")
            print(f"🔊 AI Response: \"{item[1]}, SKU {item[0]}. {item[4]} units available at {item[5]}.\"")
    
    print("\n✅ Full pipeline working!")

def main():
    """Run all demos"""
    print("🎭 OpenClaw Voice Vision - Demo Mode")
    print("No Meta glasses or real credentials needed!")
    print("\nThis demonstrates the full system with mock data.")
    
    demo_inventory_lookup()
    demo_production_status()
    demo_full_pipeline()
    
    print("\n\n" + "=" * 50)
    print("✅ All demos completed successfully!")
    print("\n📦 Mock Inventory Items:")
    for item in MOCK_INVENTORY[:3]:
        print(f"   - {item['sku']}: {item['description']}")
    
    print("\n🏭 Mock Production Jobs:")
    for job in MOCK_PRODUCTION_JOBS[:3]:
        print(f"   - {job['job_id']}: {job['customer_name']} ({job['status']})")
    
    print("\n\nNext steps:")
    print("1. Get Meta glasses for real testing")
    print("2. Get Databricks credentials for real data")
    print("3. Build iOS app in Xcode")
    print("4. Test with real hardware!")

if __name__ == "__main__":
    main()
