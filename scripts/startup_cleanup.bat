@echo off
echo Running Cleanup at Startup...
python "%~dp0\..\tests\test_cleanup.py"
pause 