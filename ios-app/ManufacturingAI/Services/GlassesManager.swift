import Foundation
import SwiftUI
import MetaWearablesSDK  // Meta's Device Access Toolkit

/// Manages connection to Meta Ray-Ban glasses
/// Handles video streaming, audio, and device state
class GlassesManager: ObservableObject {
    
    // MARK: - Published Properties
    
    @Published var connectionStatus: ConnectionStatus = .disconnected
    @Published var currentFrame: UIImage?
    @Published var isStreaming = false
    @Published var batteryLevel: Int?
    
    // MARK: - Internal Properties
    
    var videoStream: AsyncStream<CVPixelBuffer>?
    private var videoContinuation: AsyncStream<CVPixelBuffer>.Continuation?
    
    private var glassesDevice: MWDevice?
    private var datSession: MWSession?
    
    // MARK: - Enums
    
    enum ConnectionStatus: String {
        case disconnected = "Disconnected"
        case searching = "Searching..."
        case connecting = "Connecting..."
        case connected = "Connected ✅"
        case error = "Error ❌"
        
        var color: Color {
            switch self {
            case .disconnected: return .gray
            case .searching, .connecting: return .orange
            case .connected: return .green
            case .error: return .red
            }
        }
    }
    
    // MARK: - Initialization
    
    init() {
        setupVideoStream()
        initializeDAT()
    }
    
    // MARK: - Setup
    
    private func setupVideoStream() {
        videoStream = AsyncStream { continuation in
            self.videoContinuation = continuation
        }
    }
    
    private func initializeDAT() {
        // Initialize Meta Wearables SDK
        MWSDK.initialize { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    print("✅ DAT SDK initialized")
                    self?.startDeviceDiscovery()
                case .failure(let error):
                    print("❌ DAT SDK init failed: \(error)")
                    self?.connectionStatus = .error
                }
            }
        }
    }
    
    // MARK: - Device Discovery
    
    func startDeviceDiscovery() {
        guard connectionStatus == .disconnected else { return }
        
        connectionStatus = .searching
        
        MWSDK.discoverDevices { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let device):
                    print("🎯 Found glasses: \(device.name)")
                    self?.connect(to: device)
                case .failure(let error):
                    print("❌ Discovery failed: \(error)")
                    self?.connectionStatus = .error
                }
            }
        }
    }
    
    // MARK: - Connection
    
    private func connect(to device: MWDevice) {
        connectionStatus = .connecting
        
        device.connect { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    print("✅ Connected to glasses")
                    self?.glassesDevice = device
                    self?.connectionStatus = .connected
                    self?.setupSession()
                case .failure(let error):
                    print("❌ Connection failed: \(error)")
                    self?.connectionStatus = .error
                }
            }
        }
    }
    
    // MARK: - Session Setup
    
    private func setupSession() {
        guard let device = glassesDevice else { return }
        
        let config = MWSessionConfig(
            videoFormat: .jpeg(quality: 0.7, maxFPS: 1),  // ~1 FPS for AI
            audioFormat: .pcm(sampleRate: 16000, channels: 1),
            enableTelephony: false,
            enableMusic: false
        )
        
        datSession = device.createSession(config: config)
        
        // Handle incoming video frames
        datSession?.onVideoFrame = { [weak self] frameData in
            self?.processVideoFrame(frameData)
        }
        
        // Handle device state changes
        datSession?.onDeviceState = { [weak self] state in
            DispatchQueue.main.async {
                self?.batteryLevel = state.batteryLevel
            }
        }
    }
    
    // MARK: - Streaming
    
    func startStreaming() {
        guard let session = datSession else {
            print("⚠️ No active session")
            return
        }
        
        session.startStreaming { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    print("✅ Streaming started")
                    self?.isStreaming = true
                case .failure(let error):
                    print("❌ Streaming failed: \(error)")
                }
            }
        }
    }
    
    func stopStreaming() {
        datSession?.stopStreaming { [weak self] result in
            DispatchQueue.main.async {
                self?.isStreaming = false
                print("⏹️ Streaming stopped")
            }
        }
    }
    
    // MARK: - Video Processing
    
    private func processVideoFrame(_ frameData: Data) {
        // Convert JPEG data to UIImage and CVPixelBuffer
        guard let image = UIImage(data: frameData),
              let pixelBuffer = image.toCVPixelBuffer() else {
            return
        }
        
        DispatchQueue.main.async {
            self.currentFrame = image
        }
        
        // Yield to AsyncStream for Gemini
        videoContinuation?.yield(pixelBuffer)
    }
    
    // MARK: - Phone Camera Fallback
    
    func usePhoneCamera() {
        // Fallback when glasses not available
        // Would integrate with AVCaptureSession
        print("📱 Switching to phone camera mode")
    }
    
    // MARK: - Cleanup
    
    func disconnect() {
        stopStreaming()
        datSession = nil
        glassesDevice?.disconnect()
        glassesDevice = nil
        connectionStatus = .disconnected
    }
}

// MARK: - UIImage Extension

extension UIImage {
    func toCVPixelBuffer() -> CVPixelBuffer? {
        let attrs = [
            kCVPixelBufferCGImageCompatibilityKey: kCFBooleanTrue,
            kCVPixelBufferCGBitmapContextCompatibilityKey: kCFBooleanTrue
        ] as CFDictionary
        
        var pixelBuffer: CVPixelBuffer?
        let status = CVPixelBufferCreate(
            kCFAllocatorDefault,
            Int(size.width),
            Int(size.height),
            kCVPixelFormatType_32ARGB,
            attrs,
            &pixelBuffer
        )
        
        guard status == kCVReturnSuccess, let buffer = pixelBuffer else {
            return nil
        }
        
        CVPixelBufferLockBaseAddress(buffer, CVPixelBufferLockFlags(rawValue: 0))
        
        let pixelData = CVPixelBufferGetBaseAddress(buffer)
        let rgbColorSpace = CGColorSpaceCreateDeviceRGB()
        
        guard let context = CGContext(
            data: pixelData,
            width: Int(size.width),
            height: Int(size.height),
            bitsPerComponent: 8,
            bytesPerRow: CVPixelBufferGetBytesPerRow(buffer),
            space: rgbColorSpace,
            bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
        ) else {
            return nil
        }
        
        context.translateBy(x: 0, y: size.height)
        context.scaleBy(x: 1.0, y: -1.0)
        
        UIGraphicsPushContext(context)
        draw(in: CGRect(x: 0, y: 0, width: size.width, height: size.height))
        UIGraphicsPopContext()
        
        CVPixelBufferUnlockBaseAddress(buffer, CVPixelBufferLockFlags(rawValue: 0))
        
        return buffer
    }
}
