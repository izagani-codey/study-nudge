# Study Nudge

A desktop study coach that interrupts usage with active-recall prompts generated from your own PDFs.

## Features

- Mixed question formats (MCQ, True/False, Fill-in-the-Blank)
- Harder keyword selection for stronger recall practice
- Scheduler-driven popup prompts
- Control panel for PDF selection, question generation, interval control, and language mode
- Persistent app data in `~/.study-nudge` (config, progress, generated questions)

## Quick launch after downloading from GitHub

### Windows (double-click)

- Double-click `start_windows.bat`

### Terminal (Windows/macOS/Linux)

```bash
python launch.py
```

`launch.py` checks/install missing dependencies and starts the app.

## Run from source (manual)

```bash
python -m pip install -r requirements.txt
python study_nudge.py
```

## Build executable (EXE)

```bash
./scripts/build_exe.sh
```

Output binary:

- `dist/study_nudge` (or `dist/study_nudge.exe` on Windows)

## App data location

By default, user data is stored in:

- `~/.study-nudge`

You can override this with:

- `STUDY_NUDGE_HOME=/custom/path`

Stored files include:

- `config.json`
- `input.pdf`
- `questions.json`
- `progress.json`
