@echo off
set NAME=%~1
mkdir "Writeups\%NAME%" 2>nul
copy "TEMPLATE.md" "Writeups\%NAME%\README.md"
echo Created Writeups/%NAME%/README.md