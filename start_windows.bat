@echo off
setlocal

where py >nul 2>&1
if %errorlevel%==0 (
  py -3 launch.py
) else (
  python launch.py
)

endlocal
