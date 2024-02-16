@echo off

set "customtkinter_path=%USERPROFILE%\AppData\Local\Programs\Python\Python311\Lib\site-packages\customtkinter"
set "bin_dir=bin"

IF EXIST "%bin_dir%" (
    rmdir "%bin_dir%" /s /q
)

pyinstaller --onefile --icon=ico/icon.ico --noupx --noconsole main_alt2.py --add-binary="ico/icon.ico;." --add-data "%customtkinter_path%;customtkinter/"

IF EXIST dist (
    REN dist "%bin_dir%"
)

IF EXIST "%bin_dir%\main.exe" (
    cd "%bin_dir%" && REN main.exe MarioParties-4-5-6-ItemPoolGen.exe && cd ..
)

PAUSE