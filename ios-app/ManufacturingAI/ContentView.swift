import SwiftUI

struct ContentView: View {
    @StateObject private var glassesManager = GlassesManager()
    @StateObject private var geminiService = GeminiService()
    @StateObject private var audioManager = AudioManager()
    
    @State private var isShowingSettings = false
    @State private var messages: [ChatMessage] = []
    @State private var currentTranscript = ""
    
    var body: some View {
        NavigationView {
            ZStack {
                // Background
                Color.black.edgesIgnoringSafeArea(.all)
                
                VStack(spacing: 0) {
                    // Header
                    HeaderView(
                        glassesStatus: glassesManager.connectionStatus,
                        geminiStatus: geminiService.status
                    )
                    .padding(.horizontal)
                    .padding(.top, 20)
                    
                    // Camera Preview (from glasses or phone)
                    CameraPreviewView(
                        glassesManager: glassesManager,
                        currentFrame: glassesManager.currentFrame
                    )
                    .frame(height: 300)
                    .cornerRadius(16)
                    .padding()
                    
                    // Voice Activity Indicator
                    VoiceIndicatorView(
                        isListening: geminiService.isListening,
                        audioLevel: audioManager.currentAudioLevel
                    )
                    .frame(height: 60)
                    .padding(.horizontal)
                    
                    // Chat Messages
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(messages) { message in
                                MessageBubble(message: message)
                            }
                        }
                        .padding()
                    }
                    
                    // Live Transcript
                    if !currentTranscript.isEmpty {
                        Text(currentTranscript)
                            .font(.caption)
                            .foregroundColor(.gray)
                            .padding(.horizontal)
                    }
                    
                    Spacer()
                    
                    // Control Buttons
                    ControlBar(
                        glassesManager: glassesManager,
                        geminiService: geminiService,
                        onStartSession: startSession,
                        onStopSession: stopSession
                    )
                    .padding(.bottom, 30)
                }
            }
            .navigationBarHidden(true)
        }
        .onAppear {
            setupCallbacks()
        }
        .sheet(isPresented: $isShowingSettings) {
            SettingsView()
        }
    }
    
    private func setupCallbacks() {
        // Handle incoming transcripts from Gemini
        geminiService.onTranscript = { text in
            DispatchQueue.main.async {
                currentTranscript = text
            }
        }
        
        // Handle responses from Gemini
        geminiService.onResponse = { response in
            DispatchQueue.main.async {
                let message = ChatMessage(
                    id: UUID(),
                    text: response,
                    isUser: false,
                    timestamp: Date()
                )
                messages.append(message)
                currentTranscript = ""
                
                // Speak the response
                audioManager.speak(response)
            }
        }
        
        // Handle tool calls (OpenClaw integration)
        geminiService.onToolCall = { toolName, parameters in
            handleToolCall(name: toolName, parameters: parameters)
        }
    }
    
    private func startSession() {
        // Start glasses streaming
        glassesManager.startStreaming()
        
        // Start Gemini Live session
        geminiService.startSession(cameraStream: glassesManager.videoStream)
        
        // Start audio
        audioManager.startRecording()
    }
    
    private func stopSession() {
        glassesManager.stopStreaming()
        geminiService.stopSession()
        audioManager.stopRecording()
    }
    
    private func handleToolCall(name: String, parameters: [String: Any]) {
        // Forward to OpenClaw
        Task {
            do {
                let result = try await OpenClawClient.shared.executeTool(
                    name: name,
                    parameters: parameters
                )
                
                // Send result back to Gemini
                await geminiService.sendToolResult(result)
                
            } catch {
                await geminiService.sendToolResult([
                    "error": error.localizedDescription
                ])
            }
        }
    }
}

// MARK: - Supporting Types

struct ChatMessage: Identifiable {
    let id: UUID
    let text: String
    let isUser: Bool
    let timestamp: Date
}

// MARK: - Preview

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
