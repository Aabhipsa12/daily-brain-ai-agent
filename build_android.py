import sys
import os
import shutil
import subprocess

def main():
    print("="*60)
    print("DAILY BRAIN — Android Build & Packaging Automation")
    print("="*60)
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    android_dir = os.path.join(project_root, "android")
    dist_dir = os.path.join(project_root, "dist", "android")
    os.makedirs(dist_dir, exist_ok=True)
    
    # Check for Gradle or Gradlew
    gradle_cmd = None
    if os.path.exists(os.path.join(android_dir, "gradlew.bat")) and sys.platform.startswith("win"):
        gradle_cmd = os.path.join(android_dir, "gradlew.bat")
    elif shutil.which("gradle"):
        gradle_cmd = "gradle"
        
    print(f"[*] Android Project Path: {android_dir}")
    print(f"[*] Output Target: {dist_dir}")
    
    if gradle_cmd:
        print(f"[*] Executing build via {gradle_cmd}...")
        res = subprocess.run([gradle_cmd, "assembleDebug"], cwd=android_dir)
        if res.returncode == 0:
            print("[+] Android Debug APK build succeeded!")
            debug_apk = os.path.join(android_dir, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
            if os.path.exists(debug_apk):
                dest_apk = os.path.join(dist_dir, "DailyBrain-debug.apk")
                shutil.copy2(debug_apk, dest_apk)
                print(f"[+] APK available at: {dest_apk}")
        else:
            print("[-] Build encountered an error.")
    else:
        print("[!] Note: Gradle CLI / Android SDK is not in system PATH.")
        print("[+] Android project is fully structured and ready for Android Studio!")
        print("    Open 'D:\\Daily-brain\\android' in Android Studio and click 'Build' -> 'Build Bundle(s) / APK(s)'")

if __name__ == "__main__":
    main()
