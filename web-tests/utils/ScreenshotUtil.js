const fs = require('fs-extra');
const path = require('path');

class ScreenshotUtil {
    static async takeScreenshot(driver, fileName, isMobile = false) {
        const screenshot = await driver.takeScreenshot();
        const dir = isMobile ? 'reports/mobileScreenshots' : 'reports/screenshots';
        const filePath = path.join(process.cwd(), dir, `${fileName}_${Date.now()}.png`);

        await fs.ensureDir(path.dirname(filePath));
        await fs.writeFile(filePath, screenshot, 'base64');
        return filePath;
    }
}

module.exports = ScreenshotUtil;
