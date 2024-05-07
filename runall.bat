@echo off

start cmd /k "echo Running server.py... && python server.py"
echo Server.py completed.

start cmd /k "echo Running run.py... && python run.py"
echo Run.py completed.

start cmd /k "echo Running run.py again... && python run.py"
echo Run.py completed.

echo All scripts executed successfully.
