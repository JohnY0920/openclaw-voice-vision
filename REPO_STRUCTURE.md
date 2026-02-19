# Repository Structure Note

## Current Setup (Temporary)

We have **2 separate repos** during development:

### Repo 1: openclaw-voice-vision (Main)
**URL:** https://github.com/JohnY0920/openclaw-voice-vision  
**Purpose:** Production iOS app + OpenClaw skills  
**Status:** ✅ Synced to GitHub

Contents:
- iOS app for Meta glasses
- OpenClaw Python skills
- Mock data and demos
- Documentation

### Repo 2: openclaw-vision-mac (Dev Tool)
**URL:** https://github.com/JohnY0920/openclaw-vision-mac (needs creation)  
**Purpose:** macOS webcam testing app  
**Status:** ⚠️ Local only (needs push)

Contents:
- macOS native app (Xcode)
- Fast Python camera scripts
- Webcam testing tools

## Why Separate?

The macOS app is a **temporary development tool** to test the camera → AI → OpenClaw pipeline **without** needing:
- Meta glasses (not purchased yet)
- iOS app store provisioning
- Complex mobile development

Once glasses arrive, we'll primarily use the iOS app.

## Future Consolidation Plan

**TODO:** Merge macOS app into main repo under `tools/macos-camera-test/` when:
1. Meta glasses testing is complete
2. iOS app is fully functional
3. macOS tool is no longer needed for daily dev

**Reason:** Keep everything in one place for maintainability.

## Local Paths

- Main: `/Users/Phoestia/clawd/projects/manufacturing-voice-vision/`
- macOS: `/Users/Phoestia/clawd/projects/openclaw-vision-mac/`

## Sync Status

- ✅ Main repo: Synced to GitHub
- ⚠️ macOS repo: Local only (create GitHub repo manually to push)

**Action needed:** Create `openclaw-vision-mac` repo on GitHub, then:
```bash
cd /Users/Phoestia/clawd/projects/openclaw-vision-mac
git remote add origin https://github.com/JohnY0920/openclaw-vision-mac.git
git push -u origin master
```
