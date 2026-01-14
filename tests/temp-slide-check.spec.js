const { test, expect } = require('@playwright/test');

test('screenshot slide 2', async ({ page }) => {
  await page.goto('http://localhost:5001/course/cmsc173/module/1');
  await page.waitForTimeout(1000);
  await page.click('.nav-arrow.next');
  await page.waitForTimeout(500);
  await page.screenshot({ path: '/tmp/slide2.png' });
});
