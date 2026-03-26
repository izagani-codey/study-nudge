from pathlib import Path
import os

APP_NAME = "study-nudge"


def app_data_dir() -> Path:
    override = os.getenv("STUDY_NUDGE_HOME")
    if override:
        path = Path(override).expanduser()
    else:
        path = Path.home() / f".{APP_NAME}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_file(filename: str) -> Path:
    return app_data_dir() / filename
