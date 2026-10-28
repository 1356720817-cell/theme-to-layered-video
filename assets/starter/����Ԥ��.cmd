@echo off

chcp 65001 >nul

cd /d "%~dp0"

if not exist node_modules\remotion\package.json call npm install --cache work\npm-cache

call npm run dev

pause

