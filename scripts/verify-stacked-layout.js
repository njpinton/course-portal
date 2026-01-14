const { chromium } = require('@playwright/test');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('1. Navigating to http://localhost:8788/course/cmsc173/module/1...');
    await page.goto('http://localhost:8788/course/cmsc173/module/1', { waitUntil: 'networkidle' });

    // Wait a moment for any animations or transitions
    await page.waitForTimeout(1000);

    console.log('2. Clicking right arrow to go to slide 2...');
    await page.keyboard.press('ArrowRight');

    // Wait for slide transition
    await page.waitForTimeout(1000);

    console.log('3. Taking full page screenshot...');
    const screenshotPath = path.join('/Users/njpinton/projects/git/presenter_app/test-results', 'module-01-slide-02-fixed.png');
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log(`   Saved to: ${screenshotPath}`);

    console.log('4. Taking screenshot of stacked-figures-layout element...');
    const stackedElement = await page.locator('.stacked-figures-layout').first();

    if (await stackedElement.count() > 0) {
      const elementScreenshotPath = path.join('/Users/njpinton/projects/git/presenter_app/test-results', 'stacked-figures-layout-element.png');
      await stackedElement.screenshot({ path: elementScreenshotPath });
      console.log(`   Saved to: ${elementScreenshotPath}`);
    } else {
      console.log('   WARNING: .stacked-figures-layout element not found on this slide');

      // Let's check what layout elements exist
      const layoutElements = await page.locator('[class*="layout"]').all();
      console.log(`   Found ${layoutElements.length} elements with 'layout' in class name`);
      for (let i = 0; i < layoutElements.length; i++) {
        const className = await layoutElements[i].getAttribute('class');
        console.log(`   - ${className}`);
      }
    }

    console.log('\nAll tasks completed successfully!');

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
})();
