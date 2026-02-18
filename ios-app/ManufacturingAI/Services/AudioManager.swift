import Foundation
import AVFoundation

/// Manages audio recording and playback
class AudioManager: ObservableObject {
    
    @Published var currentAudioLevel: Float = 0.0
    @Published var isRecording = false
    
    private var audioEngine: AVAudioEngine?
    private var player: AVAudioPlayer?
    private var timer: Timer?
    
    private let audioSession = AVAudioSession.sharedInstance()
    
    // MARK: - Recording
    
    func startRecording() {
        do {
            try audioSession.setCategory(.playAndRecord, mode: .default)
            try audioSession.setActive(true)
            
            audioEngine = AVAudioEngine()
            
            let inputNode = audioEngine!.inputNode
            let recordingFormat = inputNode.outputFormat(forBus: 0)
            
            inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, _ in
                self?.processAudioBuffer(buffer)
            }
            
            try audioEngine!.start()
            isRecording = true
            
            // Start monitoring audio levels
            startLevelMonitoring()
            
        } catch {
            print("❌ Audio recording error: \(error)")
        }
    }
    
    func stopRecording() {
        audioEngine?.stop()
        audioEngine?.inputNode.removeTap(onBus: 0)
        audioEngine = nil
        isRecording = false
        
        timer?.invalidate()
        timer = nil
    }
    
    private func processAudioBuffer(_ buffer: AVAudioPCMBuffer) {
        // Process audio for Gemini Live
        // Convert to format expected by Gemini (PCM 16kHz)
        
        guard let channelData = buffer.floatChannelData?[0] else { return }
        let channelDataValue = channelData.pointee
        let channelDataValueArray = stride(from: 0, to: Int(buffer.frameLength), by: buffer.stride)
            .map { channelDataValue.advanced(by: $0).pointee }
        
        // Calculate RMS for level meter
        let rms = sqrt(channelDataValueArray.map { $0 * $0 }.reduce(0, +) / Float(buffer.frameLength))
        let avgPower = 20 * log10(rms)
        
        DispatchQueue.main.async {
            self.currentAudioLevel = self.normalizeAudioLevel(avgPower)
        }
    }
    
    private func normalizeAudioLevel(_ decibels: Float) -> Float {
        // Normalize -80dB to 0dB range to 0.0 to 1.0
        let minDecibels: Float = -80.0
        let maxDecibels: Float = 0.0
        
        if decibels < minDecibels {
            return 0.0
        } else if decibels >= maxDecibels {
            return 1.0
        } else {
            return (decibels - minDecibels) / (maxDecibels - minDecibels)
        }
    }
    
    private func startLevelMonitoring() {
        timer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { [weak self] _ in
            // Audio level updates happen in processAudioBuffer
        }
    }
    
    // MARK: - Playback
    
    func speak(_ text: String) {
        // Use AVSpeechSynthesizer for TTS
        // Or play pre-generated audio from Gemini
        
        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: "en-US")
        utterance.rate = 0.5
        utterance.pitchMultiplier = 1.0
        
        let synthesizer = AVSpeechSynthesizer()
        synthesizer.speak(utterance)
    }
    
    func playAudio(data: Data) {
        do {
            player = try AVAudioPlayer(data: data)
            player?.play()
        } catch {
            print("❌ Audio playback error: \(error)")
        }
    }
}
