@echo off

set SCRIPT_NAME=pyside2_test.py
nuitka --recurse-none %SCRIPT_NAME% --run --windows-disable-console