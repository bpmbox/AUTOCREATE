@echo off
echo Starting GitHub Copilot Auto Answer System...
cd /d "%~dp0\tests\Feature"
python copilot_direct_answer.py --auto
pause
