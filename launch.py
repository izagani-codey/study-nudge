import importlib.util
import subprocess
import sys
from pathlib import Path

REQUIRED_MODULES = ["PyPDF2"]


def missing_modules():
    return [name for name in REQUIRED_MODULES if importlib.util.find_spec(name) is None]


def ensure_dependencies(project_root: Path):
    missing = missing_modules()
    if not missing:
        return

    print("Installing missing dependencies:", ", ".join(missing))
    req_file = project_root / "requirements.txt"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])


def main():
    project_root = Path(__file__).resolve().parent
    ensure_dependencies(project_root)

    from ui.control_panel_app import run_control_panel

    run_control_panel()


if __name__ == "__main__":
    main()
