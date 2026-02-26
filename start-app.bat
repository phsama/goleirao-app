@echo off
echo ===================================================
echo Iniciando o Ambiente do Goleirao App...
echo ===================================================

:: Start Backend (FastAPI em porta 8000)
start "Backend - Goleirao" cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn main:app --reload"

:: Start Frontend (Servidor de Estaticos em porta 8080)
start "Frontend - Goleirao" cmd /k "cd frontend && python -m http.server 8080"

echo.
echo O Frontend estara disponivel no navegador em: http://localhost:8080
echo O Backend API estara rodando em: http://localhost:8000
echo.
echo ===================================================
echo Para parar os servidores, basta fechar as janelas pretas que se abriram!
echo ===================================================
pause
