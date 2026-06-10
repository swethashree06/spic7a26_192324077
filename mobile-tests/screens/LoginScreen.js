class LoginScreen {
    constructor(driver) {
        this.driver = driver;
        this.emailField = '//*[@text="Email"]';
        this.passwordField = '//*[@text="Password"]';
        this.loginButton = '//*[@text="Sign In"]';
    }

    async login(email, password) {
        await this.driver.$(this.emailField).setValue(email);
        await this.driver.$(this.passwordField).setValue(password);
        await this.driver.$(this.loginButton).click();
    }

    async isDisplayed() {
        return await this.driver.$(this.loginButton).isDisplayed();
    }
}

module.exports = LoginScreen;
