const { test, expect } = require('@playwright/test');

test('screenshot all slides', async ({ page }) => {
  await page.goto('http://localhost:5001/course/cmsc173/module/1');
  await page.waitForTimeout(1500);

  // Screenshot all 6 slides
  for (let i = 1; i <= 6; i++) {
    await page.screenshot({ path: `/tmp/ppt-slide${i}.png` });
    if (i < 6) {
      await page.click('#next-btn');
      await page.waitForTimeout(800);
    }
  }
});
