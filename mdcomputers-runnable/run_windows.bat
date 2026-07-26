@echo off
setlocal

if "%~1"=="" (
  echo Usage: run_windows.bat "search term" [pages]
  echo Example: run_windows.bat "external hard drive" 2
  exit /b 1
)

set SEARCH_TERM=%~1
set PAGES=%~2
if "%PAGES%"=="" set PAGES=1

if not exist .venv (
  py -3 -m venv .venv
)

call .venv\Scripts\python.exe -m pip install --upgrade pip
call .venv\Scripts\python.exe -m pip install -r requirements.txt
call .venv\Scripts\python.exe scraper.py "%SEARCH_TERM%" --pages %PAGES% -o output.csv

echo Done. Check output.csv
endlocal
