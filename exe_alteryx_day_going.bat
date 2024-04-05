@echo off
set "workflow_path="C:\Users\Benja\OneDrive\Bureau\Cac40\DataProject\ETL.yxmd""

if exist "%workflow_path%" (
    start "" "C:\Users\Benja\AppData\Local\Alteryx\bin\AlteryxGui.exe" "%workflow_path%"
    timeout /t 20 /nobreak >nul
    powershell.exe -Command "& {[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.SendKeys]::SendWait('^r')}"
) else (
    echo Le chemin spécifié vers le workflow est invalide.
    pause
)