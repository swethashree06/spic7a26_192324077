const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const LoginPage = require('../pages/LoginPage');
const DashboardPage = require('../pages/DashboardPage');
const ProfilePage = require('../pages/ProfilePage');
const ExcelReport = require('../utils/ExcelReport');
const { expect } = require('chai');

describe('Web Dashboard & Profile Tests', function() {
    let driver;
    let loginPage;
    let dashboardPage;
    let profilePage;
    const baseUrl = 'http://localhost:3000';

    before(async function() {
        const options = new chrome.Options();
        options.addArguments('--headless');
        driver = await new Builder()
            .forBrowser('chrome')
            .setChromeOptions(options)
            .build();
        loginPage = new LoginPage(driver);
        dashboardPage = new DashboardPage(driver);
        profilePage = new ProfilePage(driver);

        // Ensure logged in for these tests
        await loginPage.open(baseUrl);
        await loginPage.login('yarrapureddylakshmireddy100@gmail.com', 'password123');
    });

    after(async function() {
        await driver.quit();
    });

    it('TC_003 - Dashboard Component Visibility', async function() {
        const startTime = Date.now();
        try {
            const isLoaded = await dashboardPage.isLoaded();
            expect(isLoaded).to.be.true;

            await ExcelReport.addResult({
                id: 'TC_003',
                module: 'Dashboard',
                name: 'Visibility Check',
                status: 'PASS',
                time: `${Date.now() - startTime}ms`,
                remarks: 'Dashboard components visible'
            });
        } catch (error) {
            await ExcelReport.addResult({
                id: 'TC_003',
                module: 'Dashboard',
                name: 'Visibility Check',
                status: 'FAIL',
                time: `${Date.now() - startTime}ms`,
                remarks: error.message
            });
            throw error;
        }
    });

    it('TC_004 - Navigate to Profile', async function() {
        const startTime = Date.now();
        try {
            await dashboardPage.navigateToProfile();
            const currentUrl = await driver.getCurrentUrl();
            expect(currentUrl).to.include('/profile');

            await ExcelReport.addResult({
                id: 'TC_004',
                module: 'Profile',
                name: 'Navigation',
                status: 'PASS',
                time: `${Date.now() - startTime}ms`,
                remarks: 'Navigated to profile screen'
            });
        } catch (error) {
            await ExcelReport.addResult({
                id: 'TC_004',
                module: 'Profile',
                name: 'Navigation',
                status: 'FAIL',
                time: `${Date.now() - startTime}ms`,
                remarks: error.message
            });
            throw error;
        }
    });
});
