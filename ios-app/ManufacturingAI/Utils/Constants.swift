import Foundation

struct Constants {
    
    // MARK: - App Info
    static let appName = "Manufacturing Voice Vision AI"
    static let appVersion = "1.0.0"
    
    // MARK: - Audio
    static let audioSampleRate: Double = 16000  // 16 kHz for Gemini
    static let audioChannels = 1
    
    // MARK: - Video
    static let videoMaxFPS = 1.0  // ~1 FPS for glasses camera
    static let videoQuality: CGFloat = 0.7  // JPEG quality
    
    // MARK: - Timing
    static let connectionTimeout: TimeInterval = 30
    static let queryTimeout: TimeInterval = 60
    
    // MARK: - UI
    static let maxChatHistory = 50
    static let messageMaxWidth: CGFloat = 280
}
