@echo off
title Status of SmartHome Lamps

:READLAMPS
	cls
	echo current time: %DATE% %TIME%
	for /L %%i in (1,1,3) Do echo: && echo ++++ LAMP %%i ++++ && type .\Smart_Home_IOT\Lamp%%i\config.txt && echo: && echo:
	timeout 5 > NUL
goto READLAMPS
