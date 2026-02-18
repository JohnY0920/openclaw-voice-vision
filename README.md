# Manufacturing Voice Vision AI

Real-time voice + visual AI assistant for manufacturing operations via Meta Ray-Ban smart glasses.

Based on VisionClaw architecture, customized for industrial use cases.

## 🎯 Core Concept

**"See what you see, hear what you say, take action on your behalf"**

Workers on the factory floor can:
- 👁️ **Look** at a product/barcode/label
- 🗣️ **Ask** questions in natural language
- ✅ **Get** instant answers from ERP/Databricks data

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 META RAY-BAN GLASSES                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Camera    │  │  Microphone │  │   Speaker   │         │
│  │  (~1 FPS)   │  │  (16 kHz)   │  │  (24 kHz)   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          └────────────────┴────────────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
┌──────────────────────┐      ┌──────────────────────────┐
│   iOS / ANDROID      │      │   GEMINI LIVE API        │
│      APP             │◄────►│  (WebSocket)             │
│                      │      │  • Vision Analysis       │
│  • DAT SDK           │      │  • Voice Recognition     │
│  • Camera Stream     │      │  • Natural Language      │
│  • Audio Pipeline    │      │  • Tool Calling          │
└──────────┬───────────┘      └────────────┬─────────────┘
           │                                │
           │         ┌──────────────────────┘
           │         │
           ▼         ▼
┌─────────────────────────────────────────────────────────────┐
│                   OPENCLAW GATEWAY                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            MANUFACTURING SKILL                         │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐    │  │
│  │  │ Inventory   │ │ Production  │ │   Employee   │    │  │
│  │  │   Lookup    │ │   Status    │ │    Hours     │    │  │
│  │  └──────┬──────┘ └──────┬──────┘ └──────┬───────┘    │  │
│  │         │               │               │            │  │
│  │         └───────────────┴───────────────┘            │  │
│  │                         │                            │  │
│  │                         ▼                            │  │
│  │              ┌─────────────────────┐                 │  │
│  │              │  DATABRICKS SQL     │                 │  │
│  │              │    WAREHOUSE        │                 │  │
│  │              └─────────────────────┘                 │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📱 Supported Hardware

| Device | Status | Notes |
|--------|--------|-------|
| **Meta Ray-Ban** | Primary target | Best experience, hands-free |
| **iPhone** | Dev + Fallback | Use phone camera for testing |
| **Android** | Planned | DAT SDK available |

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Glasses | Meta Ray-Ban (Wayfarer/Headliner) |
| Mobile | Swift (iOS) + Meta DAT SDK |
| AI | Gemini Live API (multimodal) |
| Gateway | OpenClaw |
| Data | Databricks SQL Warehouse |

## 📂 Project Structure

```
Manufacturing-Voice-Vision/
├── README.md
├── ios-app/                      # iOS Application
│   ├── ManufacturingAI/
│   │   ├── AppDelegate.swift
│   │   ├── SceneDelegate.swift
│   │   ├── ContentView.swift
│   │   ├── Services/
│   │   │   ├── GlassesManager.swift      # Meta DAT SDK
│   │   │   ├── GeminiService.swift       # Gemini Live API
│   │   │   ├── OpenClawClient.swift      # OpenClaw integration
│   │   │   └── AudioManager.swift        # Audio pipeline
│   │   ├── Views/
│   │   │   ├── MainView.swift
│   │   │   ├── CameraPreviewView.swift
│   │   │   └── VoiceIndicatorView.swift
│   │   └── Utils/
│   │       ├── Secrets.swift.example
│   │       └── Constants.swift
│   ├── Podfile
│   └── ManufacturingAI.xcodeproj
├── openclaw-skill/               # OpenClaw Manufacturing Skill
│   ├── SKILL.md
│   └── scripts/
│       ├── databricks_client.py
│       ├── inventory_tool.py
│       ├── production_tool.py
│       └── employee_tool.py
├── docs/
│   ├── SETUP.md
│   ├── API_REFERENCE.md
│   └── VISIONCLAW_INTEGRATION.md
└── prototypes/
    └── camera-test/
```

## 🚀 Quick Start

### Prerequisites
- Meta Ray-Ban Smart Glasses
- iPhone with iOS 16+
- Xcode 15+
- Gemini API key
- OpenClaw Gateway running

### 1. Clone Repo
```bash
git clone https://github.com/JohnY0920/manufacturing-voice-vision.git
cd manufacturing-voice-vision
```

### 2. Setup iOS App
```bash
cd ios-app
pod install
open ManufacturingAI.xcodeproj
```

### 3. Configure Secrets
```bash
cp ManufacturingAI/Utils/Secrets.swift.example ManufacturingAI/Utils/Secrets.swift
# Edit Secrets.swift with your API keys
```

### 4. Enable Developer Mode (Meta AI App)
- Open Meta AI app on iPhone
- Settings → App Info
- Tap version number 5 times
- Enable Developer Mode

### 5. Build & Run
- Connect iPhone to Mac
- Select iPhone as target
- Build and run (Cmd+R)

## 🎤 Voice Commands

### Inventory
- *"What am I looking at?"* → Identifies item, shows stock level
- *"Scan this barcode"* → Reads QR/barcode, looks up SKU
- *"How many units of ABC123?"* → Exact inventory count
- *"Where is item XYZ?"* → Warehouse location

### Production
- *"What's the status of job 45892?"* → Job progress
- *"When will Acme Corp order be ready?"* → Completion estimate
- *"Show me today's production"* → Daily summary

### Employee
- *"How many hours this week?"* → Personal timesheet
- *"Who's on night shift?"* → Current roster

## 🔐 Security

- All API calls over TLS 1.3
- Credentials in iOS Keychain
- Role-based access control
- Audit logging for all queries
- No PII stored on device

## 📄 License

MIT License - Based on VisionClaw by Sean Liu
