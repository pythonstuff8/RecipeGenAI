import SwiftUI
import AVFoundation
import Vision

struct CameraPreview: UIViewRepresentable {
    @Binding var zoom: CGFloat
    var ocrActive: Bool = false
    var languageCode: String? = nil

    class CameraView: UIView {
        let session = AVCaptureSession()
        var previewLayer: AVCaptureVideoPreviewLayer!
        var device: AVCaptureDevice?
        var ocrActive: Bool = false
        var languageCode: String? = nil
        private let videoOutput = AVCaptureVideoDataOutput()
        
        override init(frame: CGRect) {
            super.init(frame: frame)
            setupSession()
        }
        
        required init?(coder: NSCoder) {
            fatalError("init(coder:) has not been implemented")
        }
        
        private func setupSession() {
            session.sessionPreset = .photo
            
            guard let camera = AVCaptureDevice.default(for: .video) else {
                print("No camera available")
                return
            }
            device = camera
            
            do {
                let input = try AVCaptureDeviceInput(device: camera)
                if session.canAddInput(input) {
                    session.addInput(input)
                }
            } catch {
                print("Failed to create camera input:", error)
                return
            }
            
            videoOutput.videoSettings = [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA]
            videoOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "videoQueue"))
            if session.canAddOutput(videoOutput) {
                session.addOutput(videoOutput)
            } else {
                print("Couldn't add video output")
            }
            
            previewLayer = AVCaptureVideoPreviewLayer(session: session)
            previewLayer.videoGravity = .resizeAspectFill
            layer.addSublayer(previewLayer)
            
            DispatchQueue.global(qos: .userInitiated).async {
                self.session.startRunning()
            }
        }
        
        override func layoutSubviews() {
            super.layoutSubviews()
            previewLayer.frame = bounds
            // Force landscape
            if let connection = previewLayer.connection, connection.isVideoOrientationSupported {
                connection.videoOrientation = .landscapeRight
            }
        }
        
        func setZoom(_ zoomFactor: CGFloat) {
            guard let device = device else { return }
            do {
                try device.lockForConfiguration()
                let zoom = max(1.0, min(zoomFactor, device.activeFormat.videoMaxZoomFactor))
                device.videoZoomFactor = zoom
                device.unlockForConfiguration()
            } catch {
                print("Failed to set zoom:", error)
            }
        }
        
        // MARK: - Custom OpenAI TTS call using curl-inspired API and splitting text by line
        func speakUsingOpenAITTS(_ text: String, voice: String = "coral") {
            do {
                try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
                try AVAudioSession.sharedInstance().setActive(true)
            } catch {
                print("Error configuring audio session: \(error)")
            }
            
            guard let apiKey = "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" as String?,
                  let url = URL(string: "https://api.openai.com/v1/audio/speech") else { return }
            
            let lines = text.components(separatedBy: "\n").filter { !$0.isEmpty }
            
            for (index, line) in lines.enumerated() {
                var request = URLRequest(url: url)
                request.httpMethod = "POST"
                request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
                request.setValue("application/json", forHTTPHeaderField: "Content-Type")
                
                let json: [String: Any] = [
                    "model": "gpt-4o-mini-tts",
                    "input": line,
                    "voice": voice,
                    "instructions": "Speak in a cheerful and positive tone.",
                    "response_format": "wav"
                ]
                do {
                    let jsonData = try JSONSerialization.data(withJSONObject: json)
                    request.httpBody = jsonData
                } catch {
                    print("Error serializing JSON: \(error)")
                    continue
                }
                
                DispatchQueue.global().asyncAfter(deadline: .now() + Double(index) * 1.5) {
                    let task = URLSession.shared.dataTask(with: request) { data, response, error in
                        guard let data = data, error == nil else {
                            print("Error calling TTS: \(error?.localizedDescription ?? "")")
                            return
                        }
                        DispatchQueue.main.async {
                            do {
                                let player = try AVAudioPlayer(data: data)
                                player.prepareToPlay()
                                player.play()
                            } catch {
                                print("Error creating audio player: \(error)")
                            }
                        }
                    }
                    task.resume()
                }
            }
        }
    }
    
    func makeUIView(context: Context) -> CameraView {
        return CameraView()
    }
    
    func updateUIView(_ uiView: CameraView, context: Context) {
        uiView.setZoom(zoom)
        uiView.ocrActive = ocrActive
        uiView.languageCode = languageCode
    }
}

extension CameraPreview.CameraView: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput,
                       didOutput sampleBuffer: CMSampleBuffer,
                       from connection: AVCaptureConnection) {
        if !ocrActive { return }
        
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        
        let requestHandler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:])
        let request = VNRecognizeTextRequest { [weak self] (request, error) in
            if let error = error {
                print("Error recognizing text: \(error)")
                return
            }
            guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
            var detectedText = ""
            for observation in observations {
                if let topCandidate = observation.topCandidates(1).first {
                    detectedText += topCandidate.string + "\n"
                }
            }
            if !detectedText.isEmpty {
                print("Detected Text:\n\(detectedText)")
                if let strongSelf = self {
                    let ttsVoice = strongSelf.languageCode ?? "en-US"
                    strongSelf.speakUsingOpenAITTS(detectedText, voice: ttsVoice)
                }
            }
        }
        request.recognitionLevel = .accurate
        
        do {
            try requestHandler.perform([request])
        } catch {
            print("Failed to perform OCR: \(error)")
        }
    }
}

struct ContentView: View {
    @State private var isMuted = true
    @State private var dummyValue: CGFloat = 1.0
    @State private var selectedLanguage: String? = "en-US"
    @State private var ocrStarted: Bool = false
    
    let languageDictionary: [String: String] = [
        "Arabic (Saudi Arabia)"       : "xar-SA",
        "Czech (Czech Republic)"      : "cs-CZ",
        "Danish (Denmark)"            : "da-DK",
        "German (Germany)"            : "de-DE",
        "Greek (Greece)"              : "el-GR",
        "English (Australia)"         : "en-AU",
        "English (United Kingdom)"    : "en-GB",
        "English (Ireland)"           : "en-IE",
        "English (United States)"     : "en-US",
        "English (South Africa)"      : "en-ZA",
        "Spanish (Spain)"             : "es-ES",
        "Spanish (Mexico)"            : "es-MX",
        "Finnish (Finland)"           : "fi-FI",
        "French (Canada)"             : "fr-CA",
        "French (France)"             : "fr-FR",
        "Hebrew (Israel)"             : "he-IL",
        "Hindi (India)"               : "hi-IN",
        "Hungarian (Hungary)"         : "hu-HU",
        "Indonesian (Indonesia)"      : "id-ID",
        "Italian (Italy)"             : "it-IT",
        "Japanese (Japan)"            : "ja-JP",
        "Korean (South Korea)"        : "ko-KR",
        "Dutch (Belgium)"             : "nl-BE",
        "Dutch (Netherlands)"         : "nl-NL",
        "Norwegian (Norway)"          : "no-NO",
        "Polish (Poland)"             : "pl-PL",
        "Portuguese (Brazil)"         : "pt-BR",
        "Portuguese (Portugal)"       : "pt-PT",
        "Romanian (Romania)"          : "ro-RO",
        "Russian (Russia)"            : "ru-RU",
        "Slovak (Slovakia)"           : "sk-SK",
        "Swedish (Sweden)"            : "sv-SE",
        "Thai (Thailand)"             : "th-TH",
        "Turkish (Turkey)"            : "tr-TR",
        "Chinese (Simplified, China)" : "zh-CN",
        "Chinese (Traditional, Hong Kong)" : "zh-HK",
        "Chinese (Traditional, Taiwan)"    : "zh-TW"
    ]
    
    func Change_Icon() {
        isMuted.toggle()
        ocrStarted = !isMuted
        print("Speaker button pressed. isMuted: \(isMuted), OCR Started: \(ocrStarted)")
    }
    
    var selectedLanguageName: String {
        if let code = selectedLanguage,
           let name = languageDictionary.first(where: { $0.value == code })?.key {
            return name
        }
        return "Select Language"
    }
    
    var body: some View {
        ZStack {
            CameraPreview(zoom: $dummyValue, ocrActive: ocrStarted, languageCode: selectedLanguage)
                .edgesIgnoringSafeArea(.all)
            // Overlay control panel at the bottom
            VStack {
                Spacer()
                HStack {
                    // Speaker button now comes first
                    Button(action: Change_Icon) {
                        Label("", systemImage: isMuted ? "speaker.slash.fill" : "speaker.wave.3.fill")
                            .font(.system(size: 24))
                            .foregroundColor(.white)
                    }
                    
                    // Next, the language button
                    Menu {
                        ScrollView {
                            VStack(alignment: .leading, spacing: 10) {
                                ForEach(Array(languageDictionary.keys).sorted(), id: \.self) { languageName in
                                    Button(action: {
                                        selectedLanguage = languageDictionary[languageName]
                                        print("Selected language: \(selectedLanguage ?? "")")
                                    }) {
                                        HStack {
                                            Text(languageName)
                                            Spacer()
                                            if selectedLanguage == languageDictionary[languageName] {
                                                Image(systemName: "checkmark")
                                                    .foregroundColor(.blue)
                                            }
                                        }
                                    }
                                }
                            }
                            .frame(width: 250)
                        }
                    } label: {
                        Label(selectedLanguageName, systemImage: "waveform.circle.fill")
                            .font(.system(size: 24))
                            .foregroundColor(.white)
                    }
                    
                    // The zoom slider
                    HStack {
                        Image(systemName: "minus.magnifyingglass")
                            .foregroundColor(.white)
                            .font(.system(size: 24))
                        Slider(value: $dummyValue, in: 0.5...10)
                            .accentColor(.yellow)
                        Image(systemName: "plus.magnifyingglass")
                            .foregroundColor(.white)
                            .font(.system(size: 24))
                    }
                }
                .padding()
            }
        }
    }
}

#Preview {
    ContentView()
}
