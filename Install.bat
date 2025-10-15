@echo off
echo ============================================
echo Installing Python Libraries for D2L Scripts
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install required packages
echo Installing required packages...
echo.

echo [1/3] Installing selenium...
python -m pip install selenium
echo.

echo [2/3] Installing webdriver-manager...
python -m pip install webdriver-manager
echo.

echo [3/3] Installing pandas...
python -m pip install pandas
echo.

REM Optional: Install psutil for better process cleanup
echo Installing optional package (psutil) for better Chrome cleanup...
python -m pip install psutil
echo.

echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo The following packages were installed:
echo - selenium (for browser automation)
echo - webdriver-manager (for Chrome driver management)
echo - pandas (for CSV data processing)
echo - psutil (optional, for process management)
echo.
echo You can now run your D2L scripts!
echo.
pause