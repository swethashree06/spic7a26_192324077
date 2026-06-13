const { remote } = require('webdriverio');
const ExcelReport = require('../../web-tests/utils/ExcelReport');
const ScreenshotUtil = require('../../web-tests/utils/ScreenshotUtil');
const { expect } = require('chai');

describe('Mobile Web Automation Tests (Appium)', function() {
    let driver;
    const baseUrl = 'http://10.68.220.252:3000'; // Using LAN IP for mobile access

    const capabilities = {
        platformName: 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'Android Emulator',
        'appium:browserName': 'Chrome',
        'appium:ensureWebviewsHavePages': true,
        'appium:nativeWebScreenshot': true,
        'appium:newCommandTimeout': 3600
    };

    before(async function() {
        try {
            driver = await remote({
                protocol: 'http',
                hostname: '127.0.0.1',
                port: 4723,
                path: '/',
                capabilities
            });
        } catch (error) {
            console.error('Failed to connect to Appium server. Ensure Appium is running and an emulator is active.');
            throw error;
        }
    });

    after(async function() {
        if (driver) {
            await driver.deleteSession();
        }
    });

    it('MW_001 - Mobile Web Landing Page Load', async function() {
        const startTime = Date.now();
        try {
            await driver.url(baseUrl);
            const title = await driver.getTitle();
            expect(title).to.include('SkillSyncAI');

            await ExcelReport.addResult({
                id: 'MW_001',
                module: 'MobileWeb',
                name: 'Landing Page Load',
                status: 'PASS',
                time: `${Date.now() - startTime}ms`,
                screenshot: 'N/A',
                remarks: 'Page loaded successfully on mobile browser'
            });
        } catch (error) {
            let screenshotPath = 'N/A';
            if (driver) {
                screenshotPath = await ScreenshotUtil.takeScreenshot(driver, 'MobileWeb_Load_Fail', true);
            }
            await ExcelReport.addResult({
                id: 'MW_001',
                module: 'MobileWeb',
                name: 'Landing Page Load',
                status: 'FAIL',
                time: `${Date.now() - startTime}ms`,
                screenshot: screenshotPath,
                remarks: error.message
            });
            throw error;
        }
    });

    it('MW_002 - Navigation to Login on Mobile', async function() {
        const startTime = Date.now();
        try {
            const signInBtn = await driver.$("//button[contains(text(),'Sign In')]");
            await signInBtn.click();

            const currentUrl = await driver.getUrl();
            expect(currentUrl).to.include('/auth/signin');

            await ExcelReport.addResult({
                id: 'MW_002',
                module: 'MobileWeb',
                name: 'Login Navigation',
                status: 'PASS',
                time: `${Date.now() - startTime}ms`,
                remarks: 'Navigated to sign in'
            });
        } catch (error) {
            await ExcelReport.addResult({
                id: 'MW_002',
                module: 'MobileWeb',
                name: 'Login Navigation',
                status: 'FAIL',
                time: `${Date.now() - startTime}ms`,
                remarks: error.message
            });
            throw error;
        }
    });
});
