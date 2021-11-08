set PYTHONIOENCODING=utf-8
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window --remote-debugging-port=9222 --auto-open-devtools-for-tabs
python kcauto
exit