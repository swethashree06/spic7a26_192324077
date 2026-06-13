const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const LoginPage = require('../pages/LoginPage');
const DashboardPage = require('../pages/DashboardPage');
const ExcelReport = require('../utils/ExcelReport');
const ScreenshotUtil = require('../utils/ScreenshotUtil');
const { expect } = require('chai');

const platforms = [
    { name: 'Desktop Web', mobileEmulation: null, width: 1920, height: 1080 },
    { name: 'Mobile Web (iPhone 12 Pro)', mobileEmulation: { deviceName: 'iPhone 12 Pro' }, width: 390, height: 844 }
];

const baseUrl = 'http://localhost:3000';

platforms.forEach(platform => {
    describe(`Selenium Automation - ${platform.name}`, function() {
        let driver;
        let loginPage;
        let dashboardPage;

        before(async function() {
            const options = new chrome.Options();
            options.addArguments('--headless');
            options.addArguments('--no-sandbox');
            options.addArguments('--disable-dev-shm-usage');

            if (platform.mobileEmulation) {
                options.setMobileEmulation(platform.mobileEmulation);
            }

            driver = await new Builder()
                .forBrowser('chrome')
                .setChromeOptions(options)
                .build();

            await driver.manage().window().setRect({ width: platform.width, height: platform.height });

            loginPage = new LoginPage(driver);
            dashboardPage = new DashboardPage(driver);
        });

        after(async function() {
            if (driver) await driver.quit();
        });

        it(`[${platform.name}] - Should load landing page and navigate to login`, async function() {
            const startTime = Date.now();
            const tcId = platform.mobileEmulation ? 'MW_TC_001' : 'DW_TC_001';
            try {
                await loginPage.open(baseUrl);
                const title = await driver.getTitle();
                expect(title).to.include('SkillSyncAI');

                await ExcelReport.addResult({
                    id: tcId,
                    module: platform.name,
                    name: 'Page Load',
                    status: 'PASS',
                    time: `${Date.now() - startTime}ms`,
                    remarks: 'Success'
                });
            } catch (error) {
                const screenshot = await ScreenshotUtil.takeScreenshot(driver, `Fail_${tcId}`);
                await ExcelReport.addResult({
                    id: tcId,
                    module: platform.name,
                    name: 'Page Load',
                    status: 'FAIL',
                    time: `${Date.now() - startTime}ms`,
                    screenshot: screenshot,
                    remarks: error.message
                });
                throw error;
            }
        });

        it(`[${platform.name}] - Should display login fields correctly`, async function() {
            const startTime = Date.now();
            const tcId = platform.mobileEmulation ? 'MW_TC_002' : 'DW_TC_002';
            try {
                // Already at login page from previous test if using same session,
                // but let's be explicit
                await loginPage.open(baseUrl);

                const isEmailVisible = await driver.findElement(loginPage.emailField).isDisplayed();
                const isPassVisible = await driver.findElement(loginPage.passwordField).isDisplayed();

                expect(isEmailVisible).to.be.true;
                expect(isPassVisible).to.be.true;

                await ExcelReport.addResult({
                    id: tcId,
                    module: platform.name,
                    name: 'Login UI Check',
                    status: 'PASS',
                    time: `${Date.now() - startTime}ms`,
                    remarks: 'Fields visible'
                });
            } catch (error) {
                const screenshot = await ScreenshotUtil.takeScreenshot(driver, `Fail_${tcId}`);
                await ExcelReport.addResult({
                    id: tcId,
                    module: platform.name,
                    name: 'Login UI Check',
                    status: 'FAIL',
                    time: `${Date.now() - startTime}ms`,
                    screenshot: screenshot,
                    remarks: error.message
                });
                throw error;
            }
        });
    });
});
