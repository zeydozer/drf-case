@echo off
REM Production deployment batch file for Windows

if "%1"=="build" (
  echo Building production images...
  docker-compose -f docker-compose.prod.yml build
  goto :eof
)

if "%1"=="up" (
  echo Starting production services...
  docker-compose -f docker-compose.prod.yml up -d
  goto :eof
)

if "%1"=="down" (
  echo Stopping production services...
  docker-compose -f docker-compose.prod.yml down
  goto :eof
)

if "%1"=="logs" (
  echo Showing production logs...
  docker-compose -f docker-compose.prod.yml logs -f
  goto :eof
)

if "%1"=="migrate" (
  echo Running migrations...
  docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
  goto :eof
)

if "%1"=="collectstatic" (
  echo Collecting static files...
  docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
  goto :eof
)

if "%1"=="deploy" (
  echo Starting full production deployment...
  call %0 build
  call %0 up
  timeout /t 10 /nobreak > nul
  call %0 migrate
  call %0 collectstatic
  echo Production deployment completed!
  goto :eof
)

if "%1"=="restart" (
  echo Restarting web and nginx services...
  docker-compose -f docker-compose.prod.yml restart web nginx
  goto :eof
)

if "%1"=="shell" (
  echo Opening Django shell...
  docker-compose -f docker-compose.prod.yml exec web python manage.py shell
  goto :eof
)

if "%1"=="status" (
  echo Checking service status...
  docker-compose -f docker-compose.prod.yml ps
  goto :eof
)

if "%1"=="health" (
  echo Checking health endpoint...
  curl http://localhost/health/
  goto :eof
)

REM Help
echo.
echo Production deployment commands:
echo.
echo   prod.bat build         - Build production images
echo   prod.bat up            - Start production services
echo   prod.bat down          - Stop production services
echo   prod.bat logs          - Show logs
echo   prod.bat migrate       - Run database migrations
echo   prod.bat collectstatic - Collect static files
echo   prod.bat deploy        - Full deployment (build + up + migrate + collectstatic)
echo   prod.bat restart       - Restart web and nginx services
echo   prod.bat shell         - Open Django shell
echo   prod.bat status        - Check service status
echo   prod.bat health        - Check health endpoint
echo.
