echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\v242\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\tell.exe" 37PCL051 51326 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 5496) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 21356) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 12708)
del "C:\Users\V.Chepuri\OneDrive - Cranfield University\irp\pablo\GCI\Medium_mesh\cleanup-fluent-37PCL051-21356.bat"
