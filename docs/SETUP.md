# 🚀 Manufacturing Voice Vision AI - Setup Guide

## Project Overview

Real-time voice + visual AI assistant for manufacturing, based on VisionClaw architecture by Sean Liu.

**What it does:**
- Workers wear Meta Ray-Ban glasses
- Look at products, barcodes, labels
- Ask questions in natural language
- Get instant answers from ERP/Databricks

---

## 📁 Project Structure

```
manufacturing-voice-vision/
├── ios-app/                          # iOS Application
│   ├── ManufacturingAI/
│   │   ├── AppDelegate.swift
│   │   ├── ContentView.swift         # Main UI
│   │   ├── Services/
│   │   │   ├── GlassesManager.swift  # Meta DAT SDK integration
│   │   │   ├── GeminiService.swift   # Gemini Live API
│   │   │   ├── OpenClawClient.swift  # OpenClaw gateway client
│   │   │   └── AudioManager.swift    # Audio pipeline
│   │   ├── Views/
│   │   │   └── MainView.swift        # UI components
│   │   └── Utils/
│   │       ├── Secrets.swift.example # API keys template
│   │       └── Constants.swift
│   └── Podfile                       # Dependencies
├── openclaw-skill/                   # OpenClaw backend
│   ├── SKILL.md
│   ├── scripts/                      # Tool implementations
│   └── requirements.txt
└── README.md
```

---

## 🛠️ Step-by-Step Setup

### Phase 1: Prerequisites (Do First)

#### 1.1 Hardware
- [ ] **Meta Ray-Ban Smart Glasses** ($299)
  - Order: https://www.meta.com/ray-ban-stories/
  - Recommended: Wayfarer style
- [ ] **iPhone** (iOS 16+)
- [ ] **Mac** with Xcode 15+

#### 1.2 Accounts & API Keys

**Gemini API Key:**
1. Go to https://aistudio.google.com/apikey
2. Create new key
3. Save for later

**Apple Developer Account:**
- Needed for iOS app signing
- $99/year at https://developer.apple.com

**OpenClaw Gateway:**
- Run locally or on your server
- Default: `http://localhost:3000`

**Databricks:**
- Get from your client:
  - Workspace URL
  - Personal Access Token
  - SQL Warehouse ID

---

### Phase 2: iOS App Setup

#### 2.1 Clone & Install
```bash
# Clone the repo
git clone https://github.com/JohnY0920/manufacturing-voice-vision.git
cd manufacturing-voice-vision/ios-app

# Install CocoaPods dependencies
pod install

# Open workspace (not .xcodeproj!)
open ManufacturingAI.xcworkspace
```

#### 2.2 Configure Secrets
```bash
cd ManufacturingAI/Utils
cp Secrets.swift.example Secrets.swift
```

Edit `Secrets.swift`:
```swift
struct Secrets {
    static let geminiAPIKey = "YOUR_ACTUAL_GEMINI_KEY"
    static let openClawGatewayURL = "http://localhost:3000"
    static let openClawAPIToken = "your-token"
    // ... other values
}
```

#### 2.3 Enable Meta Developer Mode (Required!)

1. Download **Meta AI** app on iPhone
2. Pair with your Ray-Ban glasses
3. Go to Settings → App Info
4. Tap **App version number 5 times**
5. Go back → Enable **Developer Mode**

---

### Phase 3: OpenClaw Skill Setup

#### 3.1 Install Dependencies
```bash
cd manufacturing-voice-vision/openclaw-skill
pip install -r requirements.txt
```

#### 3.2 Configure Environment
```bash
cp .env.example .env
# Edit .env with Databricks credentials
```

#### 3.3 Test Connection
```bash
python test_connection.py
```

---

### Phase 4: Run the App

#### 4.1 Start OpenClaw Gateway
```bash
# On your Mac
openclaw gateway start
```

#### 4.2 Build iOS App
1. In Xcode, select your iPhone as target
2. Press **Cmd+R** to build and run
3. Allow microphone and camera permissions

#### 4.3 First Test (Without Glasses)
1. Tap **"Phone"** button (uses iPhone camera)
2. Tap **"Start"** to begin Gemini session
3. Speak: *"What am I looking at?"*
4. AI should respond with visual description

#### 4.4 Test With Glasses
1. Put on Meta Ray-Ban glasses
2. Tap **"Connect"** to pair
3. Tap **"Start"** to stream
4. Look at objects and ask questions!

---

## 🎤 Voice Commands to Try

### Inventory
- *"Scan this barcode"*
- *"How many units of SKU ABC123?"*
- *"Where is this item located?"*

### Production
- *"What's the status of job 45892?"*
- *"When will Acme Corp order be ready?"*

### Employee
- *"How many hours this week?"*
- *"Who's on night shift?"*

---

## 🔧 Development Workflow

### Making Changes

**iOS App:**
```bash
cd ios-app
# Edit Swift files
# Cmd+R in Xcode to rebuild
```

**OpenClaw Skill:**
```bash
cd openclaw-skill
# Edit Python scripts
# Test: python scripts/inventory_lookup.py --sku TEST
```

### Adding New Tools

1. Create script in `openclaw-skill/scripts/`
2. Add function declaration in `GeminiService.swift`
3. Test via OpenClaw
4. Update iOS app if needed

---

## 🐛 Troubleshooting

### "No glasses found"
- Ensure glasses are charged and paired
- Check Developer Mode is enabled
- Try restarting Meta AI app

### "Gemini connection failed"
- Verify API key in Secrets.swift
- Check internet connection
- Ensure OpenClaw gateway is running

### "No data from Databricks"
- Verify credentials in .env
- Test: `python test_connection.py`
- Check warehouse is running

### App crashes
- Check Xcode console for errors
- Verify all Secrets.swift values filled
- Clean build: Cmd+Shift+K, then Cmd+Shift+Alt+K

---

## 📋 Checklist Before Client Demo

- [ ] Meta glasses paired and working
- [ ] Gemini API responding
- [ ] OpenClaw Gateway running
- [ ] Databricks connected
- [ ] Sample data loaded
- [ ] Voice commands tested
- [ ] Barcode scanning works
- [ ] Error handling graceful
- [ ] UI is clean and intuitive

---

## 🚀 Next Steps

1. **Order Meta glasses** (if not done)
2. **Get Databricks credentials** from client
3. **Set up dev environment** (follow this guide)
4. **Test with sample data**
5. **Build ERP connector** (SAP/Oracle)
6. **Pilot with 5-10 users**

---

## 📞 Support

- **VisionClaw repo:** https://github.com/sseanliu/VisionClaw
- **OpenClaw docs:** https://docs.openclaw.ai
- **Meta DAT SDK:** https://github.com/facebook/meta-wearables-dat-ios

---

## 💡 Tips

- Start with **iPhone camera mode** (no glasses needed)
- Use **sample data** for initial testing
- Test **voice commands** in quiet environment
- Keep **responses short** for voice UX
- Add **visual feedback** for all actions
