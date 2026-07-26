MDComputers Runnable Scraper

Files:
- scraper.py
- requirements.txt
- run_windows.bat

Windows quick start:
1. Extract this ZIP.
2. Open the folder.
3. Double-click or run in Command Prompt / PowerShell:
   run_windows.bat "external hard drive" 2
4. The result will be saved as output.csv

Manual run:
1. py -3 -m venv .venv
2. .\.venv\Scripts\python.exe -m pip install -r requirements.txt
3. .\.venv\Scripts\python.exe scraper.py "external hard drive" --pages 2 -o output.csv

Notes:
- Keep request volume low.
- HTML structure can change, so selectors may need updates later.
