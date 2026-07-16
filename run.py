import subprocess
import sys
import time
import os
from pathlib import Path

def main():
    # Resolve the virtual environment python interpreter path
    workspace_dir = Path(__file__).resolve().parent
    venv_path = workspace_dir / ".venv"
    if os.name == "nt":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
        
    if not python_exe.exists():
        python_exe = Path(sys.executable)

    print(f"Using Python executable: {python_exe}")
    
    # Define commands
    backend_cmd = [
        str(python_exe), "-m", "uvicorn", "app.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ]
    
    frontend_cmd = [
        str(python_exe), "-m", "streamlit", "run", str(workspace_dir / "frontend" / "app.py")
    ]
    
    print("Starting FastAPI backend...")
    backend_process = subprocess.Popen(backend_cmd, cwd=str(workspace_dir))
    
    # Wait a moment for backend to initialize
    time.sleep(2.0)
    
    print("Starting Streamlit frontend...")
    frontend_process = subprocess.Popen(frontend_cmd, cwd=str(workspace_dir))
    
    print("\nBoth services started! Press Ctrl+C to stop both services.\n")
    
    try:
        while True:
            # Check if any process has terminated
            backend_exit = backend_process.poll()
            frontend_exit = frontend_process.poll()
            
            if backend_exit is not None:
                print(f"Backend exited with code {backend_exit}")
                break
            if frontend_exit is not None:
                print(f"Frontend exited with code {frontend_exit}")
                break
                
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        # Clean up processes
        for process, name in [(backend_process, "Backend"), (frontend_process, "Frontend")]:
            if process.poll() is None:
                print(f"Terminating {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"Killing {name}...")
                    process.kill()
        print("All processes stopped.")

if __name__ == "__main__":
    main()
