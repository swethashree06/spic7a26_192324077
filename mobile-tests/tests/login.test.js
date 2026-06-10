const { remote } = require('webdriverio');
const LoginScreen = require('../screens/LoginScreen');
const ExcelReport = require('../../web-tests/utils/ExcelReport');
const { expect } = require('chai');

describe('Mobile Authentication Tests', function() {
    let driver;
    let loginScreen;

    const capabilities = {
        platformName: 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'Android Emulator',
        'appium:app': './app/build/outputs/apk/debug/app-debug.apk',
        'appium:ensureWebviewsHavePages': true,
        'appium:nativeWebScreenshot': true,
        'appium:newCommandTimeout': 3600,
        'appium:connectHardwareKeyboard': true
    };

    before(async function() {
        driver = await remote({
            protocol: 'http',
            hostname: '127.0.0.1',
            port: 4723,
            path: '/',
            capabilities
        });
        loginScreen = new LoginScreen(driver);
    });

    after(async function() {
        await driver.deleteSession();
    });

    it('MTC_001 - Mobile Login Display', async function() {
        const startTime = Date.now();
        try {
            const displayed = await loginScreen.isDisplayed();
            expect(displayed).to.be.true;

            await ExcelReport.addResult({
                id: 'MTC_001',
                module: 'MobileAuth',
                name: 'Login Screen Loaded',
                status: 'PASS',
                time: `${Date.now() - startTime}ms`,
                screenshot: 'N/A',
                remarks: 'Screen rendered correctly'
            });
        } catch (error) {
            await ExcelReport.addResult({
                id: 'MTC_001',
                module: 'MobileAuth',
                name: 'Login Screen Loaded',
                status: 'FAIL',
                time: `${Date.now() - startTime}ms`,
                screenshot: 'Failure_Screenshot',
                remarks: error.message
            });
            throw error;
        }
    });
});
