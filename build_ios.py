import sys
import os
import shutil
import subprocess

def main():
    print("="*60)
    print("DAILY BRAIN — iOS Build & Archive Assistant")
    print("="*60)
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    ios_dir = os.path.join(project_root, "ios")
    dist_dir = os.path.join(project_root, "dist", "ios")
    os.makedirs(dist_dir, exist_ok=True)
    
    print(f"[*] iOS Project Path: {ios_dir}")
    print(f"[*] Output Target: {dist_dir}")
    
    xcodebuild_cmd = shutil.which("xcodebuild")
    if xcodebuild_cmd and sys.platform == "darwin":
        print("[*] macOS environment detected. Executing xcodebuild...")
        proj_path = os.path.join(ios_dir, "DailyBrain.xcodeproj")
        cmd = [
            xcodebuild_cmd,
            "-project", proj_path,
            "-scheme", "DailyBrain",
            "-configuration", "Release",
            "-destination", "generic/platform=iOS",
            "clean", "build"
        ]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print("[+] iOS build succeeded!")
        else:
            print("[-] Build failed. Check Xcode compilation logs.")
    else:
        print("[+] iOS Xcode Project is configured and ready!")
        print("    1. Transfer 'ios/' folder to macOS or open directly in Xcode.")
        print("    2. Open 'ios/DailyBrain.xcodeproj'.")
        print("    3. Select your development team under Signing & Capabilities.")
        print("    4. Click Product -> Archive to generate an IPA or distribute to TestFlight.")

if __name__ == "__main__":
    main()
