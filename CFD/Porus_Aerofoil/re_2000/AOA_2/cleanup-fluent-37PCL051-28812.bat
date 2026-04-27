echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\v242\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\tell.exe" 37PCL051 62669 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 30628) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 28812) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 13388)
del "C:\Users\V.Chepuri\OneDrive - Cranfield University\irp\pablo\AOA_2\cleanup-fluent-37PCL051-28812.bat"
