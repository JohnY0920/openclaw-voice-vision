import SwiftUI

struct HeaderView: View {
    let glassesStatus: GlassesManager.ConnectionStatus
    let geminiStatus: GeminiService.SessionStatus
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text("Manufacturing AI")
                    .font(.headline)
                    .foregroundColor(.white)
                
                HStack(spacing: 8) {
                    StatusBadge(
                        label: "Glasses",
                        color: glassesStatus.color
                    )
                    
                    StatusBadge(
                        label: "AI",
                        color: geminiStatus == .active ? .green : .gray
                    )
                }
            }
            
            Spacer()
            
            Button(action: {
                // Open settings
            }) {
                Image(systemName: "gear")
                    .foregroundColor(.white)
                    .font(.title2)
            }
        }
    }
}

struct StatusBadge: View {
    let label: String
    let color: Color
    
    var body: some View {
        Text(label)
            .font(.caption2)
            .fontWeight(.medium)
            .foregroundColor(.white)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(color.opacity(0.3))
            .cornerRadius(8)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(color, lineWidth: 1)
            )
    }
}

struct CameraPreviewView: View {
    @ObservedObject var glassesManager: GlassesManager
    let currentFrame: UIImage?
    
    var body: some View {
        ZStack {
            // Camera feed
            if let frame = currentFrame {
                Image(uiImage: frame)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } else {
                // Placeholder
                Rectangle()
                    .fill(Color.gray.opacity(0.2))
                    .overlay(
                        VStack {
                            Image(systemName: "camera.fill")
                                .font(.largeTitle)
                                .foregroundColor(.gray)
                            Text("Camera Feed")
                                .foregroundColor(.gray)
                        }
                    )
            }
            
            // Scanning overlay
            ScanningOverlay()
        }
    }
}

struct ScanningOverlay: View {
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Corner brackets
                CornerBracket(position: .topLeft, size: geometry.size)
                CornerBracket(position: .topRight, size: geometry.size)
                CornerBracket(position: .bottomLeft, size: geometry.size)
                CornerBracket(position: .bottomRight, size: geometry.size)
                
                // Center reticle
                Circle()
                    .stroke(Color.green.opacity(0.5), lineWidth: 2)
                    .frame(width: 60, height: 60)
                
                Crosshair()
                    .stroke(Color.green.opacity(0.3), lineWidth: 1)
                    .frame(width: 100, height: 100)
            }
        }
    }
}

enum CornerPosition {
    case topLeft, topRight, bottomLeft, bottomRight
}

struct CornerBracket: View {
    let position: CornerPosition
    let size: CGSize
    
    var body: some View {
        let bracketLength: CGFloat = 30
        let bracketThickness: CGFloat = 3
        let offset: CGFloat = 20
        
        ZStack {
            // Horizontal line
            Rectangle()
                .fill(Color.green)
                .frame(width: bracketLength, height: bracketThickness)
                .position(x: horizontalX(offset: offset), y: horizontalY(offset: offset))
            
            // Vertical line
            Rectangle()
                .fill(Color.green)
                .frame(width: bracketThickness, height: bracketLength)
                .position(x: verticalX(offset: offset), y: verticalY(offset: offset))
        }
    }
    
    private func horizontalX(offset: CGFloat) -> CGFloat {
        switch position {
        case .topLeft, .bottomLeft: return offset + 15
        case .topRight, .bottomRight: return size.width - offset - 15
        }
    }
    
    private func horizontalY(offset: CGFloat) -> CGFloat {
        switch position {
        case .topLeft, .topRight: return offset
        case .bottomLeft, .bottomRight: return size.height - offset
        }
    }
    
    private func verticalX(offset: CGFloat) -> CGFloat {
        switch position {
        case .topLeft, .bottomLeft: return offset
        case .topRight, .bottomRight: return size.width - offset
        }
    }
    
    private func verticalY(offset: CGFloat) -> CGFloat {
        switch position {
        case .topLeft, .topRight: return offset + 15
        case .bottomLeft, .bottomRight: return size.height - offset - 15
        }
    }
}

struct Crosshair: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let center = CGPoint(x: rect.midX, y: rect.midY)
        
        // Horizontal line
        path.move(to: CGPoint(x: rect.minX, y: center.y))
        path.addLine(to: CGPoint(x: rect.maxX, y: center.y))
        
        // Vertical line
        path.move(to: CGPoint(x: center.x, y: rect.minY))
        path.addLine(to: CGPoint(x: center.x, y: rect.maxY))
        
        return path
    }
}

struct VoiceIndicatorView: View {
    let isListening: Bool
    let audioLevel: Float
    
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: isListening ? "waveform" : "mic.slash")
                .foregroundColor(isListening ? .green : .gray)
                .font(.title2)
            
            if isListening {
                // Audio level bars
                HStack(spacing: 2) {
                    ForEach(0..<10) { i in
                        AudioBar(
                            index: i,
                            level: audioLevel,
                            totalBars: 10
                        )
                    }
                }
            }
            
            Spacer()
            
            Text(isListening ? "Listening..." : "Tap to start")
                .font(.caption)
                .foregroundColor(.gray)
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(12)
    }
}

struct AudioBar: View {
    let index: Int
    let level: Float
    let totalBars: Int
    
    var body: some View {
        let threshold = Float(index) / Float(totalBars)
        let isActive = level > threshold
        
        Rectangle()
            .fill(isActive ? Color.green : Color.gray.opacity(0.3))
            .frame(width: 4, height: 20)
            .cornerRadius(2)
            .animation(.easeInOut(duration: 0.05), value: isActive)
    }
}

struct MessageBubble: View {
    let message: ChatMessage
    
    var body: some View {
        HStack {
            if message.isUser {
                Spacer()
            }
            
            Text(message.text)
                .padding(12)
                .background(message.isUser ? Color.blue : Color.gray.opacity(0.2))
                .foregroundColor(message.isUser ? .white : .primary)
                .cornerRadius(16)
                .frame(maxWidth: 280, alignment: message.isUser ? .trailing : .leading)
            
            if !message.isUser {
                Spacer()
            }
        }
    }
}

struct ControlBar: View {
    @ObservedObject var glassesManager: GlassesManager
    @ObservedObject var geminiService: GeminiService
    let onStartSession: () -> Void
    let onStopSession: () -> Void
    
    var body: some View {
        HStack(spacing: 20) {
            // Connect Glasses Button
            Button(action: {
                glassesManager.startDeviceDiscovery()
            }) {
                VStack {
                    Image(systemName: "eyeglasses")
                        .font(.title2)
                    Text("Connect")
                        .font(.caption)
                }
                .foregroundColor(.white)
                .frame(width: 70, height: 70)
                .background(glassesManager.connectionStatus == .connected ? Color.green : Color.blue)
                .cornerRadius(16)
            }
            
            // Main Action Button
            Button(action: {
                if geminiService.status == .active {
                    onStopSession()
                } else {
                    onStartSession()
                }
            }) {
                VStack {
                    Image(systemName: geminiService.status == .active ? "stop.fill" : "mic.fill")
                        .font(.largeTitle)
                    Text(geminiService.status == .active ? "Stop" : "Start")
                        .font(.caption)
                }
                .foregroundColor(.white)
                .frame(width: 90, height: 90)
                .background(geminiService.status == .active ? Color.red : Color.green)
                .clipShape(Circle())
                .shadow(radius: 10)
            }
            
            // Phone Camera Fallback
            Button(action: {
                glassesManager.usePhoneCamera()
            }) {
                VStack {
                    Image(systemName: "iphone")
                        .font(.title2)
                    Text("Phone")
                        .font(.caption)
                }
                .foregroundColor(.white)
                .frame(width: 70, height: 70)
                .background(Color.gray)
                .cornerRadius(16)
            }
        }
    }
}

struct SettingsView: View {
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        NavigationView {
            List {
                Section(header: Text("API Keys")) {
                    Text("Configure in Secrets.swift")
                        .foregroundColor(.gray)
                }
                
                Section(header: Text("Connection")) {
                    Text("OpenClaw Gateway: \(Secrets.openClawGatewayURL)")
                    Text("Databricks: \(Secrets.databricksHost)")
                }
                
                Section(header: Text("About")) {
                    Text("Manufacturing Voice Vision AI v1.0")
                    Text("Based on VisionClaw by Sean Liu")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
            }
            .navigationTitle("Settings")
            .navigationBarItems(trailing: Button("Done") {
                presentationMode.wrappedValue.dismiss()
            })
        }
    }
}
