import Foundation
import GoogleGenerativeAI  // Gemini SDK

/// Manages Gemini Live API connection for real-time voice + vision
class GeminiService: ObservableObject {
    
    // MARK: - Published Properties
    
    @Published var status: SessionStatus = .idle
    @Published var isListening = false
    
    // MARK: - Callbacks
    
    var onTranscript: ((String) -> Void)?
    var onResponse: ((String) -> Void)?
    var onToolCall: ((String, [String: Any]) -> Void)?
    
    // MARK: - Private Properties
    
    private var liveSession: GenerativeModel?
    private var chat: Chat?
    private var isSessionActive = false
    
    private let systemPrompt = """
    You are an AI assistant for manufacturing floor workers. You can see through their smart glasses \
    and help them with inventory, production status, and employee information.
    
    When you need to query data, use the available tools:
    - inventory_lookup: Check stock levels by SKU or barcode
    - production_status: Get job status and completion estimates
    - employee_hours: Check timesheet data
    
    Keep responses concise and natural for voice interaction.
    """
    
    // MARK: - Enums
    
    enum SessionStatus: String {
        case idle = "Idle"
        case connecting = "Connecting..."
        case active = "Active 🎤"
        case error = "Error"
    }
    
    // MARK: - Session Management
    
    func startSession(cameraStream: AsyncStream<CVPixelBuffer>?) {
        guard !isSessionActive else { return }
        
        status = .connecting
        
        Task {
            do {
                // Initialize Gemini Live
                let config = GenerationConfig(
                    temperature: 0.7,
                    topP: 0.95,
                    maxOutputTokens: 1024
                )
                
                let model = GenerativeModel(
                    name: "gemini-1.5-flash-live",
                    apiKey: Secrets.geminiAPIKey,
                    generationConfig: config,
                    systemInstruction: systemPrompt
                )
                
                // Start live session with function calling
                let tools: [Tool] = [
                    createInventoryTool(),
                    createProductionTool(),
                    createEmployeeTool()
                ]
                
                chat = model.startLiveChat(tools: tools) { [weak self] event in
                    self?.handleLiveEvent(event)
                }
                
                // Start camera stream if available
                if let stream = cameraStream {
                    await startVideoStream(stream)
                }
                
                await MainActor.run {
                    self.isSessionActive = true
                    self.status = .active
                    self.isListening = true
                }
                
            } catch {
                await MainActor.run {
                    self.status = .error
                    print("❌ Gemini session error: \(error)")
                }
            }
        }
    }
    
    func stopSession() {
        chat?.end()
        chat = nil
        isSessionActive = false
        isListening = false
        status = .idle
    }
    
    // MARK: - Video Stream
    
    private func startVideoStream(_ stream: AsyncStream<CVPixelBuffer>) async {
        Task {
            for await frame in stream {
                guard isSessionActive else { break }
                
                // Send frame to Gemini for visual context
                let image = UIImage(cvPixelBuffer: frame)
                let content = Content.image(image)
                
                try? await chat?.sendMessage(content)
            }
        }
    }
    
    // MARK: - Event Handling
    
    private func handleLiveEvent(_ event: LiveEvent) {
        DispatchQueue.main.async {
            switch event {
            case .transcript(let text):
                self.onTranscript?(text)
                
            case .response(let text):
                self.onResponse?(text)
                
            case .functionCall(let name, let args):
                self.handleFunctionCall(name: name, args: args)
                
            case .error(let error):
                self.status = .error
                print("❌ Live event error: \(error)")
                
            case .listeningState(let isListening):
                self.isListening = isListening
            }
        }
    }
    
    private func handleFunctionCall(name: String, args: [String: Any]) {
        print("🔧 Function call: \(name) with args: \(args)")
        onToolCall?(name, args)
    }
    
    func sendToolResult(_ result: [String: Any]) async {
        let jsonData = try? JSONSerialization.data(withJSONObject: result)
        let jsonString = String(data: jsonData ?? Data(), encoding: .utf8) ?? "{}"
        
        let content = Content.text("Tool result: \(jsonString)")
        try? await chat?.sendMessage(content)
    }
    
    // MARK: - Tool Definitions
    
    private func createInventoryTool() -> Tool {
        return Tool.functionDeclarations([
            FunctionDeclaration(
                name: "inventory_lookup",
                description: "Look up inventory information by SKU or barcode",
                parameters: [
                    "sku": Schema.string(description: "Stock Keeping Unit identifier"),
                    "barcode": Schema.string(description: "Barcode or QR code value")
                ],
                requiredParameters: []
            )
        ])
    }
    
    private func createProductionTool() -> Tool {
        return Tool.functionDeclarations([
            FunctionDeclaration(
                name: "production_status",
                description: "Get production job status and completion estimates",
                parameters: [
                    "job_id": Schema.string(description: "Production job identifier"),
                    "customer": Schema.string(description: "Customer name for order lookup")
                ],
                requiredParameters: []
            )
        ])
    }
    
    private func createEmployeeTool() -> Tool {
        return Tool.functionDeclarations([
            FunctionDeclaration(
                name: "employee_hours",
                description: "Check employee timesheet and hours worked",
                parameters: [
                    "employee_id": Schema.string(description: "Employee identifier"),
                    "date_range": Schema.string(description: "Date range like 'this week' or 'last month'")
                ],
                requiredParameters: ["employee_id"]
            )
        ])
    }
}
