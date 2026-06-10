const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const LoginPage = require('../pages/LoginPage');
const DashboardPage = require('../pages/DashboardPage');
const ExcelReport = require('../utils/ExcelReport');
const ScreenshotUtil = require('../utils/ScreenshotUtil');
const { expect } = require('chai');

describe('Web Authentication Tests', function() {
    let driver;
    let loginPage;
    let dashboardPage;
    const baseUrl = 'http://localhost:3000';

    before(async function() {
        const options = new chrome.Options();
        options.addArguments('--headless'); // Running headless for server environment
        driver = await new Builder()
            .forBrowser('chrome')
            .setChromeOptions(options)
            .build();
        loginPage = new LoginPage(driver);
        dashboardPage = new DashboardPage(driver);
    });

    after(async function() {
        await ExcelReport.saveReport();
        await driver.quit();
    });

    it('TC_001 - Login with valid credentials', async function() {
        const startTime = Date.now();
        try {
            await loginPage.open(baseUrl);
            await loginPage.login('yarrapureddylakshmireddy100@gmail.com', 'password123');
            const isDashboard = await dashboardPage.isLoaded();
            expect(isDashboard).to.be.true;

            await ExcelReport.addResult({
                id: 'TC_001',
                module: 'Auth',
                name: 'Valid Login',
                status: 'PASS',
                time: `${Date.now() - startTime}ms`,
                screenshot: 'N/A',
                remarks: 'Login successful'
            });
        } catch (error) {
            const screenshotPath = await ScreenshotUtil.takeScreenshot(driver, 'Login_Failure');
            await ExcelReport.addResult({
                id: 'TC_001',
                module: 'Auth',
                name: 'Valid Login',
                status: 'FAIL',
                time: `${Date.now() - startTime}ms`,
                screenshot: screenshotPath,
                remarks: error.message
            });
            throw error;
        }
    });

    it('TC_002 - Registration Navigation', async function() {
        const startTime = Date.now();
        try {
            await loginPage.open(baseUrl);
            await loginPage.clickSignUp();
            const currentUrl = await driver.getCurrentUrl();
            expect(currentUrl).to.include('/auth/signup');

            await ExcelReport.addResult({
                id: 'TC_002',
                module: 'Auth',
                name: 'Registration Navigation',
                status: 'PASS',
                time: `${Date.now() - startTime}ms`,
                screenshot: 'N/A',
                remarks: 'Navigated to signup'
            });
        } catch (error) {
            const screenshotPath = await ScreenshotUtil.takeScreenshot(driver, 'Signup_Nav_Failure');
            await ExcelReport.addResult({
                id: 'TC_002',
                module: 'Auth',
                name: 'Registration Navigation',
                status: 'FAIL',
                time: `${Date.now() - startTime}ms`,
                screenshot: screenshotPath,
                remarks: error.message
            });
            throw error;
        }
    });
});
