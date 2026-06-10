class ProfileScreen {
    constructor(driver) {
        this.driver = driver;
        this.profileHeader = '//*[@text="Account Information"]';
        this.editButton = '//*[@text="Edit Picture"]';
        this.logoutButton = '//*[@text="Sign Out"]';
    }

    async clickLogout() {
        await this.driver.$(this.logoutButton).click();
    }

    async isAtProfile() {
        return await this.driver.$(this.profileHeader).isDisplayed();
    }
}

module.exports = ProfileScreen;
