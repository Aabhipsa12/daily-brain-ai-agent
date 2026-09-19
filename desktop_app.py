import os
import sys
import time
import socket
import subprocess
import threading

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def start_streamlit_server(port: int = 8501):
    """Spawns the local Streamlit server in the background if not already running."""
    if is_port_in_use(port):
        print(f"Streamlit server already running on port {port}.")
        return None

    project_dir = "D:/Daily-brain"
    app_path = os.path.join(project_dir, "app.py")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.address",
        "127.0.0.1",
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false"
    ]
    
    startupinfo = None
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process = subprocess.Popen(
        cmd,
        cwd=project_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        startupinfo=startupinfo
    )
    
    # Wait until server is reachable
    for _ in range(30):
        if is_port_in_use(port):
            break
        time.sleep(0.5)
        
    return process

def main():
    import webview

    port = 8501
    server_process = start_streamlit_server(port)
    url = f"http://127.0.0.1:{port}"

    def on_closed():
        if server_process:
            try:
                server_process.terminate()
                server_process.wait(timeout=2)
            except Exception:
                try:
                    server_process.kill()
                except Exception:
                    pass

    # Create native desktop window
    window = webview.create_window(
        title="Daily Brain — AI Task Management Agent",
        url=url,
        width=1280,
        height=820,
        min_size=(900, 600),
        background_color="#0E1117",
        text_select=True
    )
    
    window.events.closed += on_closed
    webview.start(private_mode=False)

if __name__ == "__main__":
    main()
