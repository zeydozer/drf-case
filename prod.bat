@echo off
REM Production deployment batch file for Windows

REM Usage: prod.bat <command> [environment]
if "%2"=="prod" (
  echo Using production configuration...
  set CONFIG_FILE=docker-compose.prod.yml
) else (
  echo Using development configuration...
  set CONFIG_FILE=docker-compose.yml
)

if "%1"=="up" (
  echo Starting production services...
  docker-compose -f %CONFIG_FILE% up --build -d
  goto :eof
)

if "%1"=="down" (
  echo Stopping production services...
  docker-compose -f %CONFIG_FILE% down -v
  goto :eof
)

if "%1"=="logs" (
  echo Showing production logs...
  docker-compose -f %CONFIG_FILE% logs -f
  goto :eof
)

if "%1"=="restart" (
  echo Restarting web and nginx services...
  docker-compose -f %CONFIG_FILE% restart
  goto :eof
)

if "%1"=="status" (
  echo Checking service status...
  docker-compose -f %CONFIG_FILE% ps
  goto :eof
)

if "%1"=="health" (
  echo Checking health endpoint...
  curl http://localhost/health/
  goto :eof
)

if "%1"=="cleancache" (
  echo Clearing Python cache files...
  echo Removing __pycache__ directories...
  for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
  echo Removing .pyc files...
  for /r %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
  echo Removing .pyo files...
  for /r %%f in (*.pyo) do @if exist "%%f" del /q "%%f"
  echo Removing Celery cache files...
  if exist celery_results.sqlite del /q celery_results.sqlite
  if exist celerybeat-schedule del /q celerybeat-schedule
  echo Cache cleanup completed!
  goto :eof
)

if "%1"=="test" (
  echo Running tests...
  docker exec drf_case-web-1 python manage.py test users.tests flights.tests crew.tests
  goto :eof
)

REM Help
echo.
echo Production deployment commands:
echo.
echo   prod.bat up            - Start production services
echo   prod.bat down          - Stop production services
echo   prod.bat logs          - Show logs
echo   prod.bat restart       - Restart web and nginx services
echo   prod.bat status        - Check service status
echo   prod.bat health        - Check health endpoint
echo   prod.bat cleancache    - Clear Python cache files (__pycache__, .pyc, .pyo)
echo   prod.bat test          - Run tests
echo.
