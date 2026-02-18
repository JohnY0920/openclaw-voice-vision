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
from scripts.inventory_lookup import InventoryLookup
from scripts.production_status import ProductionStatus

def demo_inventory_lookup():
    """Demo: Look up inventory by SKU"""
    print("\n📦 INVENTORY LOOKUP DEMO")
    print("=" * 50)
    
    lookup = InventoryLookup(client=MockDatabricksClient())
    
    # Test SKU lookup
    print("\n1. Looking up SKU 'ABC123'...")
    result = lookup.lookup_by_sku("ABC123")
    print(f"   Found: {result.get('found')}")
    print(f"   Description: {result.get('description')}")
    print(f"   Available: {result.get('quantity_available')} units")
    
    # Test barcode lookup
    print("\n2. Looking up barcode '987654321098'...")
    result = lookup.lookup_by_barcode("987654321098")
    print(f"   Found: {result.get('found')}")
    print(f"   SKU: {result.get('sku')}")
    print(f"   Location: {result.get('location')}")
    
    # Test voice response
    print("\n3. Voice response format:")
    print(f"   \"{lookup.format_voice_response(result)}\"")
    
    # Test low stock
    print("\n4. Low stock items:")
    result = lookup.get_low_stock_items()
    if result.get('result', {}).get('data_array'):
        for row in result['result']['data_array']:
            print(f"   - {row[0]}: {row[2]} units (reorder at {row[3]})")

def demo_production_status():
    """Demo: Check production jobs"""
    print("\n\n🏭 PRODUCTION STATUS DEMO")
    print("=" * 50)
    
    ps = ProductionStatus(client=MockDatabricksClient())
    
    # Test job lookup
    print("\n1. Checking job 'JOB001'...")
    result = ps.get_job_status("JOB001")
    print(f"   Customer: {result.get('customer')}")
    print(f"   Status: {result.get('status')}")
    print(f"   Progress: {result.get('quantity_produced')}/{result.get('quantity_ordered')}")
    
    # Test voice response
    print("\n2. Voice response format:")
    print(f"   \"{ps.format_voice_response(result)}\"")
    
    # Test overdue jobs
    print("\n3. Overdue jobs:")
    result = ps.get_overdue_jobs()
    if result.get('result', {}).get('data_array'):
        for row in result['result']['data_array'][:3]:
            print(f"   - {row[0]}: {row[1]} (Due: {row[4]})")

def demo_full_pipeline():
    """Demo: Simulate the full voice + vision pipeline"""
    print("\n\n🎭 FULL PIPELINE DEMO")
    print("=" * 50)
    print("\nSimulating: User wearing glasses scans a barcode...")
    print("\n👤 User: 'Scan this barcode'")
    print("🤖 AI: (Processes visual input from camera)")
    print("📷 Camera: Detects barcode '123456789012'")
    print("🔍 Tool Call: inventory_lookup(barcode='123456789012')")
    
    lookup = InventoryLookup(client=MockDatabricksClient())
    result = lookup.lookup_by_barcode("123456789012")
    response = lookup.format_voice_response(result)
    
    print(f"📊 Database: Returns inventory data")
    print(f"🔊 AI Response: \"{response}\"")
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
    print("\nNext steps:")
    print("1. Get Meta glasses for real testing")
    print("2. Get Databricks credentials for real data")
    print("3. Build iOS app in Xcode")
    print("4. Test with real hardware!")

if __name__ == "__main__":
    main()
