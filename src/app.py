import sys
import subprocess
from pathlib import Path
import venv

# 1. Define supported Python version bounds
MIN_PYTHON = (3, 12)
MAX_PYTHON = (3, 15)

def check_python_version():
    current_version = sys.version_info[:2]
    if not (MIN_PYTHON <= current_version <= MAX_PYTHON):
        min_str = f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
        max_str = f"{MAX_PYTHON[0]}.{MAX_PYTHON[1]}"
        print(f"[X] ERROR: Python {sys.version.split()[0]} is not supported.")
        print(f"    Please run this script using Python {min_str} through {max_str}.")
        sys.exit(1)
    print(f"[✓] Python version check passed ({sys.version.split()[0]})")

def build_environment():
    
    to_install = [
        "numpy==2.5.3",
        "Panda3D==1.10.16",
        "ursina==8.3.0",
        "pillow==12.3.0",
        "screeninfo==0.8.1",
        "panda3d-gltf==1.3.0",
        "panda3d-simplepbr==0.13.1"
    ]
    
    print("[..] Creating VENV \".venv\" environment...")
    venv_dir = Path(__file__).parent / ".venv"
    venv.create(venv_dir, with_pip=True)
    print("[✓] \".venv\" folder created successfully!")
    
    if sys.platform == "win32":
        python_bin = venv_dir / "Scripts" / "python.exe"
        pip_bin = venv_dir / "Scripts" / "pip.exe"
    else:
        python_bin = venv_dir / "bin" / "python"
        pip_bin = venv_dir / "bin" / "pip"

    # 3. Execute commands directly using the .venv binaries
    for item in to_install:
        subprocess.run([str(pip_bin), "install", item], check=True)
    print(f"[✓] All packages installed successfully. (Use python \"app.py --run\" to run)")

def build():
    check_python_version()
    build_environment()

def run():
    venv_dir = Path(__file__).parent / ".venv"

    # 1. Resolve OS-specific venv Python binary
    if sys.platform == "win32":
        python_bin = venv_dir / "Scripts" / "python.exe"
    else:
        python_bin = venv_dir / "bin" / "python"

    # 2. Check if .venv exists
    if not python_bin.exists():
        print("[X] ERROR: Virtual environment not found!")
        print("    Please run 'python build.py --build' first.")
        sys.exit(1)

    # 3. Locate your application entry point (adjust path if needed)
    main_script = Path(__file__).parent / "src" / "main.py"
    if not main_script.exists():
        main_script = Path(__file__).parent / "main.py"

    if not main_script.exists():
        print(f"[X] ERROR: Could not find main application script at {main_script}")
        sys.exit(1)

    print(f"[*] Launching application with .venv Python...")
    try:
        # Pass any extra command-line arguments to your main script
        extra_args = sys.argv[2:]
        subprocess.run([str(python_bin), str(main_script)] + extra_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[X] Application exited with error code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n[*] Application stopped by user.")


if __name__ == "__main__":
    # Prevent IndexError if script is run without arguments
    if len(sys.argv) < 2:
        print("Usage: python build.py [--build | --run]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "--build":
        build()
    elif command == "--run":
        run()
    else:
        print(f"[X] Unknown option: '{command}'")
        print("Usage: python build.py [--build | --run]")