::/==================================================================\::
:: Name: start_venv.bat                                               ::
:: Description:                                                       ::
::   Will activate projects venv for current working directory        ::
:: Tip:                                                               ::
::   You can simply type deactivate to leave the virtual enviroment   ::
::\==================================================================/::
@echo off

set VENV_NAME=ffxiv_auto_venv

:: Enter and activate Virtual Enviroment
pushd %~dp0\%VENV_NAME%%\Scripts
call activate
:: Back to working directory now in venv
popd

@echo on
