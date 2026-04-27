echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\v242\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\tell.exe" 37PCL051 64629 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 20608) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 26752) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 31128)
del "C:\Users\V.Chepuri\OneDrive - Cranfield University\irp\pablo\AOA_4\cleanup-fluent-37PCL051-26752.bat"
