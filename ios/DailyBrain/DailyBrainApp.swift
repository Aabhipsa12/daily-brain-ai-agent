import SwiftUI
import WebKit
import Network

@main
struct DailyBrainApp: App {
    var body: some Scene {
        WindowGroup {
            MainContainerView()
                .preferredColorScheme(.dark)
        }
    }
}

class NetworkMonitor: ObservableObject {
    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue(label: "NetworkMonitor")
    @Published var isConnected: Bool = true

    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                self?.isConnected = (path.status == .satisfied)
            }
        }
        monitor.start(queue: queue)
    }

    deinit {
        monitor.cancel()
    }
}

struct MainContainerView: View {
    @StateObject private var network = NetworkMonitor()
    @State private var reloadKey = UUID()

    var body: some View {
        ZStack {
            Color(red: 14/255, green: 17/255, blue: 23/255)
                .edgesIgnoringSafeArea(.all)

            if network.isConnected {
                DailyBrainWebView(url: URL(string: "https://daily-brain-agent.streamlit.app")!)
                    .id(reloadKey)
                    .edgesIgnoringSafeArea(.all)
            } else {
                OfflineFallbackView(onRetry: {
                    reloadKey = UUID()
                })
            }
        }
    }
}

struct OfflineFallbackView: View {
    var onRetry: () -> Void

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "wifi.slash")
                .font(.system(size: 64))
                .foregroundColor(Color(red: 99/255, green: 102/255, blue: 241/255))
            
            Text("Connection Required")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.white)

            Text("Daily Brain requires an internet connection to sync your tasks and run the AI agent.")
                .font(.subheadline)
                .foregroundColor(Color(red: 148/255, green: 163/255, blue: 184/255))
                .multilineTextAlignment(.center)
                .padding(.horizontal, 32)

            Button(action: onRetry) {
                Text("Retry Connection")
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .background(Color(red: 99/255, green: 102/255, blue: 241/255))
                    .cornerRadius(8)
            }
            .padding(.top, 10)
        }
        .padding()
    }
}

struct DailyBrainWebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        
        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        webView.uiDelegate = context.coordinator
        webView.scrollView.bounces = true
        webView.isOpaque = false
        webView.backgroundColor = UIColor(red: 14/255, green: 17/255, blue: 23/255, alpha: 1.0)
        
        let request = URLRequest(url: url)
        webView.load(request)
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, WKNavigationDelegate, WKUIDelegate {
        var parent: DailyBrainWebView

        init(_ parent: DailyBrainWebView) {
            self.parent = parent
        }
        
        // Handle iOS 15+ media capture permissions (Microphone for Voice Input)
        func webView(_ webView: WKWebView, requestMediaCapturePermissionFor origin: WKSecurityOrigin, initiatedByFrame frame: WKFrameInfo, type: WKMediaCaptureType, decisionHandler: @escaping (WKPermissionDecision) -> Void) {
            decisionHandler(.grant)
        }
    }
}
