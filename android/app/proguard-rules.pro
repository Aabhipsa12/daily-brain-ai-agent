# Daily Brain Android ProGuard Rules
-keepattributes *Annotation*
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep Kotlin reflect and coroutines if used
-dontwarn kotlin.**
-dontwarn androidx.webkit.**
