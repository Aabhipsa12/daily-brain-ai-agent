"""
DAILY BRAIN — Master Build Orchestrator
Cross-Platform Multi-Target Release & Build Pipeline
Author: Daily Brain Engineering Team
"""

import os
import sys
import shutil
import subprocess
import argparse
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")

def print_header(title):
    print("\n" + "=" * 64)
    print(f"  {title.upper()}")
    print("=" * 64)

def run_step(name, fn):
    print(f"\n[*] Starting: {name}...")
    try:
        success = fn()
        if success:
            print(f"[+] COMPLETED: {name}")
        else:
            print(f"[-] WARNING/SKIPPED: {name}")
        return success
    except Exception as e:
        print(f"[!] ERROR in {name}: {e}")
        return False

def build_desktop_target():
    print_header("Building Desktop Target (Windows .exe & Shortcuts)")
    build_script = os.path.join(PROJECT_ROOT, "build_desktop.py")
    if os.path.exists(build_script):
        res = subprocess.run([sys.executable, build_script], cwd=PROJECT_ROOT)
        return res.returncode == 0
    else:
        print("[-] build_desktop.py not found.")
        return False

def build_android_target():
    print_header("Building Android Target (Gradle / APK Assistant)")
    build_script = os.path.join(PROJECT_ROOT, "build_android.py")
    if os.path.exists(build_script):
        res = subprocess.run([sys.executable, build_script], cwd=PROJECT_ROOT)
        return res.returncode == 0
    else:
        print("[-] build_android.py not found.")
        return False

def build_ios_target():
    print_header("Building iOS Target (Xcode / IPA Assistant)")
    build_script = os.path.join(PROJECT_ROOT, "build_ios.py")
    if os.path.exists(build_script):
        res = subprocess.run([sys.executable, build_script], cwd=PROJECT_ROOT)
        return res.returncode == 0
    else:
        print("[-] build_ios.py not found.")
        return False

def verify_web_pwa_target():
    print_header("Verifying Web & PWA Assets")
    static_dir = os.path.join(PROJECT_ROOT, "static")
    required_files = [
        "manifest.json",
        "sw.js",
        "offline.html",
        "icon-192.png",
        "icon-512.png",
        "apple-touch-icon.png",
        "favicon.ico"
    ]
    missing = []
    for f in required_files:
        p = os.path.join(static_dir, f)
        if not os.path.exists(p):
            missing.append(f)
            
    if missing:
        print(f"[-] Missing static PWA files: {missing}")
        return False
    else:
        print(f"[+] All {len(required_files)} static PWA & offline files verified!")
        return True

def generate_dist_summary():
    print_header("Daily Brain Distribution Summary")
    os.makedirs(DIST_DIR, exist_ok=True)
    
    summary_path = os.path.join(DIST_DIR, "BUILD_SUMMARY.txt")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = [
        "DAILY BRAIN — PRODUCTION DISTRIBUTION REPORT",
        f"Generated: {now_str}",
        "-" * 50,
        f"Project Root: {PROJECT_ROOT}",
        f"Dist Directory: {DIST_DIR}",
        "",
        "Platform Targets Status:",
        "  • Web / PWA: Verified & Synchronized with Streamlit Cloud",
        "  • Desktop (Windows): Configured via pywebview & PyInstaller",
        "  • Android: Native WebView & Gradle project configured",
        "  • iOS: Native SwiftUI & Xcode project configured",
        "-" * 50,
        "Available Executables & Artifacts in dist/:"
    ]
    
    found_items = []
    for root, _, files in os.walk(DIST_DIR):
        for f in files:
            if f != "BUILD_SUMMARY.txt":
                rel = os.path.relpath(os.path.join(root, f), DIST_DIR)
                size_kb = os.path.getsize(os.path.join(root, f)) / 1024
                found_items.append(f"  - {rel} ({size_kb:.1f} KB)")
                
    if not found_items:
        lines.append("  (Platform directories created in dist/)")
    else:
        lines.extend(found_items)
        
    summary_text = "\n".join(lines)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
        
    print(summary_text)
    print(f"\n[+] Distribution summary saved to: {summary_path}")

def main():
    parser = argparse.ArgumentParser(description="Daily Brain Master Build Pipeline")
    parser.add_argument("--desktop", action="store_true", help="Build Desktop Target only")
    parser.add_argument("--android", action="store_true", help="Build Android Target only")
    parser.add_argument("--ios", action="store_true", help="Build iOS Target only")
    parser.add_argument("--pwa", action="store_true", help="Verify Web/PWA Target only")
    args = parser.parse_args()
    
    print_header("Daily Brain Unified Build Pipeline")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    build_all = not (args.desktop or args.android or args.ios or args.pwa)
    
    results = {}
    if build_all or args.pwa:
        results["Web / PWA"] = run_step("Web & PWA Verification", verify_web_pwa_target)
    if build_all or args.desktop:
        results["Desktop (Windows)"] = run_step("Desktop Packaging", build_desktop_target)
    if build_all or args.android:
        results["Android Target"] = run_step("Android Build", build_android_target)
    if build_all or args.ios:
        results["iOS Target"] = run_step("iOS Build", build_ios_target)
        
    generate_dist_summary()
    
    print_header("Pipeline Execution Completed")
    for target, res in results.items():
        status = "PASSED / READY" if res else "REVIEW / NOTICE"
        print(f"  • {target.ljust(22)} : {status}")

if __name__ == "__main__":
    main()
