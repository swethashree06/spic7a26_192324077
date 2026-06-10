const { By, until } = require('selenium-webdriver');

class ProfilePage {
    constructor(driver) {
        this.driver = driver;
        this.accountInfo = By.xpath("//span[text()='Account Information']");
        this.settings = By.xpath("//span[text()='App Settings']");
        this.logoutButton = By.xpath("//span[text()='Sign Out']");
    }

    async clickLogout() {
        const btn = await this.driver.findElement(this.logoutButton);
        await this.driver.executeScript("arguments[0].scrollIntoView()", btn);
        await btn.click();
    }

    async navigateToSettings() {
        await this.driver.findElement(this.settings).click();
    }
}

module.exports = ProfilePage;
