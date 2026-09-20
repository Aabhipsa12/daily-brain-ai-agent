import os
import sys
import subprocess
import shutil

def build():
    print("=== Building Daily Brain Standalone Desktop Package ===")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Collect data files
    datas = [
        ("app.py", "."),
        ("main.py", "."),
        ("tasks.json", "."),
        (".env.example", "."),
        ("app.ico", "."),
        ("static", "static"),
        (".streamlit", ".streamlit")
    ]
    
    data_args = []
    sep = ";" if sys.platform == "win32" else ":"
    for src, dst in datas:
        src_path = os.path.join(project_dir, src)
        if os.path.exists(src_path):
            data_args.extend(["--add-data", f"{src_path}{sep}{dst}"])
            
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "DailyBrain",
        "--icon", os.path.join(project_dir, "app.ico"),
        "--collect-all", "streamlit",
        "--collect-all", "google.genai",
        "--collect-all", "webview",
        *data_args,
        os.path.join(project_dir, "desktop_app.py")
    ]
    
    print("Running PyInstaller...")
    res = subprocess.run(cmd, cwd=project_dir)
    if res.returncode == 0:
        print("\n[SUCCESS] Daily Brain desktop binary compiled in dist/DailyBrain/DailyBrain.exe")
    else:
        print("\n[ERROR] PyInstaller build failed with exit code:", res.returncode)

if __name__ == "__main__":
    build()