echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\v242\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\tell.exe" 37PCL051 63251 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 25876) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 18480) 
if /i "%LOCALHOST%"=="37PCL051" (%KILL_CMD% 15768)
del "C:\Users\V.Chepuri\OneDrive - Cranfield University\irp\pablo\re_200000\AOA_12\cleanup-fluent-37PCL051-18480.bat"
