::/==================================================================\::
:: Name: start_ffxiv_auto.bat                                         ::
:: Description:                                                       ::
::   Will start up FFIXV atuo program and venv                        ::
::\==================================================================/::
@echo off

set VENV_NAME=ffxiv_auto_venv

:: Enter and activate Virtual Enviroment
pushd %~dp0\%VENV_NAME%%\Scripts
call activate
:: Back to working directory now in venv
popd

:: Start FFXIV
pushd "C:\\Program Files (x86)\\SquareEnix\\FINAL FANTASY XIV - A Realm Reborn\\boot"
start ffxivboot.exe
popd

:: Start FFXIV atuo
pushd %~dp0\src
start python main.py
popd

@echo on
