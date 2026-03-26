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


## New: Generate questions from websites

1. Open the app (`python launch.py` or double-click `start_windows.bat`).
2. Paste a full URL (must start with `http://` or `https://`) in the **Website URL** field.
3. Click **Generate from Website**.
4. Start Study Mode to get popup questions from that webpage content.

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
