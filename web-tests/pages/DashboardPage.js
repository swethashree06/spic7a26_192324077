const { By, until } = require('selenium-webdriver');

class DashboardPage {
    constructor(driver) {
        this.driver = driver;
        this.matchScore = By.xpath("//h2[text()='RESUME MATCH SCORE']");
        this.uploadButton = By.xpath("//button[contains(text(),'Upload New Resume')]");
        this.profileNav = By.xpath("//a[contains(@href, '/dashboard/profile')]");
        this.roadmapNav = By.xpath("//a[contains(@href, '/dashboard/roadmap')]");
    }

    async isLoaded() {
        await this.driver.wait(until.elementLocated(this.matchScore), 10000);
        return await this.driver.findElement(this.matchScore).isDisplayed();
    }

    async navigateToProfile() {
        await this.driver.findElement(this.profileNav).click();
    }

    async clickUpload() {
        await this.driver.findElement(this.uploadButton).click();
    }
}

module.exports = DashboardPage;
