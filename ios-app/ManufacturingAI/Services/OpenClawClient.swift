import Foundation

/// Client for OpenClaw Gateway
/// Handles tool execution and skill management
class OpenClawClient {
    
    static let shared = OpenClawClient()
    
    private let baseURL: String
    private let apiToken: String
    
    private init() {
        self.baseURL = Secrets.openClawGatewayURL
        self.apiToken = Secrets.openClawAPIToken
    }
    
    /// Execute a tool via OpenClaw
    func executeTool(name: String, parameters: [String: Any]) async throws -> [String: Any] {
        let url = URL(string: "\(baseURL)/api/tools/execute")!
        
        let requestBody: [String: Any] = [
            "tool": name,
            "parameters": parameters,
            "skill": "manufacturing-core"
        ]
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(apiToken)", forHTTPHeaderField: "Authorization")
        request.httpBody = try JSONSerialization.data(withJSONObject: requestBody)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw OpenClawError.requestFailed
        }
        
        guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            throw OpenClawError.invalidResponse
        }
        
        return json
    }
    
    /// Check if OpenClaw Gateway is available
    func checkHealth() async -> Bool {
        guard let url = URL(string: "\(baseURL)/health") else {
            return false
        }
        
        do {
            let (_, response) = try await URLSession.shared.data(from: url)
            return (response as? HTTPURLResponse)?.statusCode == 200
        } catch {
            return false
        }
    }
    
    enum OpenClawError: Error {
        case requestFailed
        case invalidResponse
        case toolNotFound
        case executionFailed(String)
    }
}
