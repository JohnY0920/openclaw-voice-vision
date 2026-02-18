# 🏭 Manufacturing Voice Vision AI

**Real-time voice + visual AI for manufacturing operations via Meta Ray-Ban smart glasses.**

Inspired by [VisionClaw](https://github.com/sseanliu/VisionClaw) by Sean Liu.

---

## ✨ What It Does

Workers on the factory floor can:

1. **👁️ Look** at a product, barcode, or label through Meta glasses
2. **🗣️ Ask** questions in natural language
3. **✅ Get** instant answers from ERP/Databricks data

### Example Interactions

> *"Scan this barcode"*  
> → Glasses scan QR → AI looks up SKU → *"Part ABC123, 450 units in stock, Warehouse A"

> *"What's the status of the Acme order?"*  
> → AI queries production → *"Job #45892, 80% complete, finishing tomorrow 2 PM"

> *"How many hours did I work this week?"*  
> → AI checks timesheet → *"32 hours logged, 8 hours remaining"

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  META GLASSES   │────▶│   iOS APP       │────▶│  GEMINI LIVE    │
│  • Camera       │     │  • DAT SDK      │     │  • Vision       │
│  • Microphone   │     │  • Audio Pipe   │     │  • Voice        │
│  • Speaker      │◀────│  • OpenClaw     │◀────│  • Tool Calls   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                              ┌──────────────────────────┘
                              ▼
                    ┌─────────────────┐
                    │  OPENCLAW       │
                    │  • Manufacturing│
                    │    Skill        │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
            ┌──────────────┐  ┌──────────────┐
            │ DATABRICKS   │  │ ERP/CRM      │
            │ SQL Warehouse│  │ Systems      │
            └──────────────┘  └──────────────┘
```

---

## 📦 What's Included

### iOS Application (`ios-app/`)
- Full SwiftUI interface
- Meta DAT SDK integration
- Gemini Live API connection
- Audio pipeline (mic + speaker)
- Camera preview with scanning overlay

### OpenClaw Skill (`openclaw-skill/`)
- Databricks SQL connector
- Inventory lookup tools
- Production status queries
- Employee hours tracking

---

## 🚀 Quick Start

### 1. Clone
```bash
git clone https://github.com/JohnY0920/manufacturing-voice-vision.git
cd manufacturing-voice-vision
```

### 2. Setup iOS App
```bash
cd ios-app
pod install
open ManufacturingAI.xcworkspace
```

### 3. Configure
```bash
# iOS Secrets
cp ManufacturingAI/Utils/Secrets.swift.example ManufacturingAI/Utils/Secrets.swift
# Edit with your API keys

# OpenClaw Skill
cd ../openclaw-skill
cp .env.example .env
# Edit with Databricks credentials
```

### 4. Run
- Start OpenClaw Gateway
- Build & run in Xcode
- Pair with Meta glasses
- Start voice session!

See [docs/SETUP.md](docs/SETUP.md) for detailed instructions.

---

## 🛠️ Requirements

| Component | Requirement |
|-----------|-------------|
| **Hardware** | Meta Ray-Ban glasses, iPhone, Mac |
| **iOS** | 16.0+ |
| **Xcode** | 15.0+ |
| **APIs** | Gemini API key, OpenClaw, Databricks |

---

## 📁 Project Structure

```
manufacturing-voice-vision/
├── ios-app/              # iOS Swift application
│   ├── ManufacturingAI/
│   │   ├── Services/     # Core logic (DAT, Gemini, OpenClaw)
│   │   ├── Views/        # UI components
│   │   └── Utils/        # Helpers & config
│   └── Podfile
├── openclaw-skill/       # Python backend tools
│   └── scripts/          # Databricks connectors
└── docs/                 # Documentation
    └── SETUP.md          # Detailed setup guide
```

---

## 🎯 Use Cases

| Role | Example Query |
|------|---------------|
| **Warehouse Worker** | *"Where is SKU ABC123?"* |
| **Floor Supervisor** | *"What's today's production?"* |
| **Quality Inspector** | *"Scan this barcode for specs"* |
| **Manager** | *"Show overdue jobs"* |

---

## 🔐 Security

- TLS 1.3 for all connections
- Credentials in iOS Keychain
- Role-based access control
- Audit logging
- No PII stored on device

---

## 🤝 Credits

- **Architecture:** Based on [VisionClaw](https://github.com/sseanliu/VisionClaw) by Sean Liu
- **Agent Layer:** [OpenClaw](https://github.com/nichochar/openclaw)
- **AI:** Google Gemini Live API
- **Glasses:** Meta Ray-Ban with DAT SDK

---

## 📄 License

MIT License - See LICENSE file

---

## 🚧 Status

**Phase:** Development (Week 1)  
**Next:** Testing with sample data, ERP integration

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for roadmap.
