@echo off
echo ===================================================
echo   SkillSyncAI Appium Web Automation Runner
echo ===================================================
echo.
echo Prerequisites:
echo 1. Appium Server running (appium)
echo 2. Android Emulator or Device connected (adb devices)
echo 3. Chrome installed on the mobile device
echo.
echo Starting tests...
echo.
npx mocha mobile-tests/tests/mobile_web.test.js --timeout 60000
echo.
echo Tests completed. Checking reports...
ls reports/excel/
pause
