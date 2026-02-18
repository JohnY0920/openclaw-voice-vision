---
name: manufacturing-voice-vision
description: Real-time voice + vision AI for manufacturing via Meta Ray-Ban glasses. Handles inventory, production, and employee queries.
homepage: https://github.com/JohnY0920/manufacturing-voice-vision
metadata:
  {
    "openclaw":
      {
        "emoji": "🏭",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Manufacturing Voice Vision Skill

AI assistant skill for manufacturing operations via voice and visual input from smart glasses.

## Capabilities

### Inventory Management
- `inventory_lookup` - Check stock levels by SKU or barcode
- `inventory_search` - Fuzzy search by description
- `low_stock_alert` - Get items below reorder point

### Production Tracking
- `production_status` - Check job status by ID
- `customer_orders` - Get all orders for a customer
- `daily_production` - Today's production summary
- `overdue_jobs` - Jobs past due date

### Employee Management
- `employee_hours` - Get timesheet data
- `employee_search` - Find employees by name/ID
- `department_roster` - Who's on shift

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Test connection
python test_connection.py
```

## Tools

See `scripts/` directory for all tool implementations.

## Integration

This skill is called by the iOS/Android app via OpenClaw Gateway when Gemini Live triggers a function call.

## Data Flow

```
Glasses → iOS App → Gemini Live → OpenClaw → This Skill → Databricks → Response
```
