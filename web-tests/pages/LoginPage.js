const { By, until } = require('selenium-webdriver');

class LoginPage {
    constructor(driver) {
        this.driver = driver;
        this.emailField = By.css('input[type="email"]');
        this.passwordField = By.css('input[type="password"]');
        this.loginButton = By.xpath("//button[text()='Sign In']");
        this.signUpLink = By.linkText("Sign up for free");
        this.forgotPasswordLink = By.linkText("Forgot password?");
    }

    async open(baseUrl) {
        await this.driver.get(`${baseUrl}/auth/signin`);
    }

    async login(email, password) {
        await this.driver.findElement(this.emailField).sendKeys(email);
        await this.driver.findElement(this.passwordField).sendKeys(password);
        await this.driver.findElement(this.loginButton).click();
    }

    async clickSignUp() {
        await this.driver.findElement(this.signUpLink).click();
    }

    async clickForgotPassword() {
        await this.driver.findElement(this.forgotPasswordLink).click();
    }
}

module.exports = LoginPage;
