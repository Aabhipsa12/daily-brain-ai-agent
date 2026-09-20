package com.dailybrain.app

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.view.View
import android.webkit.*
import android.widget.Button
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var offlineLayout: View
    private lateinit var btnRetry: Button
    private var pendingPermissionRequest: PermissionRequest? = null

    // Daily Brain Live Streamlit Cloud Endpoint
    private val appUrl = "https://daily-brain-agent.streamlit.app"

    private val requestAudioPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { isGranted ->
            if (isGranted) {
                pendingPermissionRequest?.grant(pendingPermissionRequest?.resources)
            } else {
                pendingPermissionRequest?.deny()
                Toast.makeText(this, "Microphone permission is required for voice input", Toast.LENGTH_LONG).show()
            }
            pendingPermissionRequest = null
        }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        // Switch from Splash Theme back to Standard Theme
        setTheme(R.style.Theme_DailyBrain)
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        swipeRefresh = findViewById(R.id.swipe_refresh)
        webView = findViewById(R.id.web_view)
        offlineLayout = findViewById(R.id.layout_offline)
        btnRetry = findViewById(R.id.btn_retry)

        // Configure Swipe Refresh styling
        swipeRefresh.setColorSchemeColors(ContextCompat.getColor(this, R.color.primary_color))
        swipeRefresh.setProgressBackgroundColorSchemeColor(0xFF1E293B.toInt())

        // Configure WebView settings for modern web app & AI agent capabilities
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            mediaPlaybackRequiresUserGesture = false
            useWideViewPort = true
            loadWithOverviewMode = true
            allowFileAccess = true
            cacheMode = WebSettings.LOAD_DEFAULT
        }

        // WebChromeClient to handle HTML5 microphone & audio capture permissions
        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest) {
                if (request.resources.contains(PermissionRequest.RESOURCE_AUDIO_CAPTURE)) {
                    if (ContextCompat.checkSelfPermission(
                            this@MainActivity,
                            Manifest.permission.RECORD_AUDIO
                        ) == PackageManager.PERMISSION_GRANTED
                    ) {
                        request.grant(request.resources)
                    } else {
                        pendingPermissionRequest = request
                        requestAudioPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
                    }
                } else {
                    request.grant(request.resources)
                }
            }
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                swipeRefresh.isRefreshing = true
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                swipeRefresh.isRefreshing = false
                offlineLayout.visibility = View.GONE
                webView.visibility = View.VISIBLE
            }

            override fun onReceivedError(
                view: WebView?,
                errorCode: Int,
                description: String?,
                failingUrl: String?
            ) {
                if (!isNetworkAvailable()) {
                    showOfflineScreen()
                }
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                if (request?.isForMainFrame == true && !isNetworkAvailable()) {
                    showOfflineScreen()
                }
            }
        }

        swipeRefresh.setOnRefreshListener {
            loadApp()
        }

        btnRetry.setOnClickListener {
            loadApp()
        }

        loadApp()
    }

    private fun loadApp() {
        if (isNetworkAvailable()) {
            offlineLayout.visibility = View.GONE
            webView.visibility = View.VISIBLE
            webView.loadUrl(appUrl)
        } else {
            showOfflineScreen()
        }
    }

    private fun showOfflineScreen() {
        swipeRefresh.isRefreshing = false
        webView.visibility = View.GONE
        offlineLayout.visibility = View.VISIBLE
    }

    private fun isNetworkAvailable(): Boolean {
        val connectivityManager =
            getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }

    override fun onBackPressed() {
        if (webView.visibility == View.VISIBLE && webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
