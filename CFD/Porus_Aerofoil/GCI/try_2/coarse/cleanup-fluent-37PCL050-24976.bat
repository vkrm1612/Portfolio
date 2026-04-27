echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\v242\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\tell.exe" 37PCL050 62969 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\v242\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="37PCL050" (%KILL_CMD% 24312) 
if /i "%LOCALHOST%"=="37PCL050" (%KILL_CMD% 24976) 
if /i "%LOCALHOST%"=="37PCL050" (%KILL_CMD% 31400)
del "C:\Users\V.Chepuri\OneDrive - Cranfield University\irp\pablo\GCI\try_2\coarse\cleanup-fluent-37PCL050-24976.bat"
