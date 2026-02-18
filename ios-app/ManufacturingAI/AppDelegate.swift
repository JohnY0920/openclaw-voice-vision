import SwiftUI
import AVFoundation

@main
struct ManufacturingAIApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
        // Request permissions
        requestPermissions()
        return true
    }
    
    private func requestPermissions() {
        // Microphone permission
        AVAudioSession.sharedInstance().requestRecordPermission { granted in
            print("Microphone permission: \(granted)")
        }
        
        // Camera permission (for phone mode)
        AVCaptureDevice.requestAccess(for: .video) { granted in
            print("Camera permission: \(granted)")
        }
    }
}
