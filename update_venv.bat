::/=============================================================\::
:: Name: update_venv.bat                                         ::
:: Description:                                                  ::
::     This script will set up or update the projects virtual    ::
::     enviroment and installed packages                         ::
::\=============================================================/::
@echo off

set VENV_NAME=ffxiv_auto_venv

:: Create and/or enter virtual enviroment
call python -m venv %VENV_NAME%
pushd %~dp0\%VENV_NAME%\Scripts
call activate

:: Install/Upate required pip packages
call python -m pip install -r ../../pip_packages.txt --upgrade

:: Back to starting directory
call deactivate
popd

@echo on
