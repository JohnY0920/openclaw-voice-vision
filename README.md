# 🔮 OpenClaw Voice Vision

**Real-time voice + visual AI assistant for Meta Ray-Ban smart glasses.**

Give your OpenClaw agent eyes and ears. See what you see, hear what you say, and take action on your behalf.

Based on [VisionClaw](https://github.com/sseanliu/VisionClaw) by Sean Liu.

---

## ✨ What It Does

Connect your Meta Ray-Ban glasses to OpenClaw for hands-free AI assistance:

- **👁️ Visual Understanding** - AI sees through your glasses camera
- **🗣️ Voice Commands** - Natural language interaction
- **🛠️ Agent Actions** - Execute any OpenClaw skill
- **✅ Instant Results** - Search, message, shop, control smart home, and more

### Example Use Cases

> *"What am I looking at?"*  
> → AI analyzes the scene and describes it

> *"Search for this on Amazon"*  
> → Visual product search and price comparison

> *"Add milk to my shopping list"*  
> → Updates your todo/shopping list

> *"Send a message to John saying I'll be late"*  
> → Routes through WhatsApp/Telegram/iMessage

> *"Turn off the living room lights"*  
> → Smart home control

> *"Check my calendar for tomorrow"*  
> → Calendar and scheduling

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  META GLASSES   │────▶│   iOS APP       │────▶│  GEMINI LIVE    │
│  • Camera       │     │  • DAT SDK      │     │  • Vision       │
│  • Microphone   │     │  • Audio Pipe   │     │  • Voice        │
│  • Speaker      │◀────│  • OpenClaw     │◀────│  • Tool Calls   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
          │                                              │
          │                    ┌─────────────────────────┘
          │                    ▼
          │          ┌─────────────────┐
          │          │  OPENCLAW       │
          │          │  GATEWAY        │
          │          │                 │
          │          │  56+ Skills:    │
          │          │  • Search       │
          │          │  • Messaging    │
          │          │  • Shopping     │
          │          │  • Smart Home   │
          │          │  • Calendar     │
          │          │  • Notes        │
          │          │  • Custom...    │
          │          └─────────────────┘
          │                    │
          └────────────────────┘
          (Optional: Custom Skills for Enterprise)
```

---

## 🚀 Quick Start

### 1. Clone
```bash
git clone https://github.com/JohnY0920/openclaw-voice-vision.git
cd openclaw-voice-vision
```

### 2. Setup iOS App
```bash
cd ios-app
pod install
open OpenClawVoiceVision.xcworkspace
```

### 3. Configure
```bash
# iOS Secrets
cp OpenClawVoiceVision/Utils/Secrets.swift.example OpenClawVoiceVision/Utils/Secrets.swift
# Edit with your API keys
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
| **APIs** | Gemini API key, OpenClaw Gateway |

---

## 📁 Project Structure

```
openclaw-voice-vision/
├── ios-app/                    # iOS Swift application
│   ├── OpenClawVoiceVision/
│   │   ├── Services/           # Core logic (DAT, Gemini, OpenClaw)
│   │   ├── Views/              # UI components
│   │   └── Utils/              # Helpers & config
│   └── Podfile
├── openclaw-skill/             # Optional: Custom skills
│   └── scripts/                # Your custom tools
└── docs/                       # Documentation
    └── SETUP.md
```

---

## 🎯 Use Cases

| Category | Example Commands |
|----------|-----------------|
| **Shopping** | *"Search for this on Amazon"*, *"Compare prices"* |
| **Messaging** | *"Send a message to John"*, *"Reply to Sarah"* |
| **Smart Home** | *"Turn off the lights"*, *"Set thermostat to 72"* |
| **Search** | *"What am I looking at?"*, *"Search the web for this"* |
| **Productivity** | *"Add to my shopping list"*, *"Set a reminder"* |
| **Enterprise** | *"Check inventory"*, *"Look up customer"* (custom skills) |

---

## 🔐 Security

- TLS 1.3 for all connections
- Credentials in iOS Keychain
- No data stored on device
- All actions go through your OpenClaw Gateway

---

## 🤝 Credits

- **Based on:** [VisionClaw](https://github.com/sseanliu/VisionClaw) by Sean Liu
- **Agent Layer:** [OpenClaw](https://github.com/nichochar/openclaw)
- **AI:** Google Gemini Live API
- **Glasses:** Meta Ray-Ban with DAT SDK

---

## 📄 License

MIT License - See LICENSE file

---

## 🚧 Status

**Phase:** Development (Week 1)  
**Next:** Testing, skill integration

This is an open-source project. Contributions welcome!
