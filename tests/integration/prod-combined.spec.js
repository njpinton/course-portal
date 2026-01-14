const { test, expect } = require('@playwright/test');

const PROD_URL = 'https://presenterapp-nine.vercel.app';

test.describe('Production Combined Module 0', () => {
  test('Module 0 loads with all slides', async ({ page }) => {
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.goto(`${PROD_URL}/course/cmsc173/module/00`, { waitUntil: 'networkidle' });

    // Wait for slides to load
    await page.waitForFunction(() => {
      const counter = document.querySelector('.slide-counter');
      if (!counter) return false;
      const text = counter.textContent || '';
      const match = text.match(/(\d+)/g);
      if (!match) return false;
      return parseInt(match[match.length - 1]) > 15;
    }, { timeout: 15000 });

    const slideCount = await page.evaluate(() => {
      const counter = document.querySelector('.slide-counter');
      const text = counter?.textContent || '';
      const match = text.match(/(\d+)/g);
      return match ? parseInt(match[match.length - 1]) : 0;
    });

    console.log(`Production Module 0: ${slideCount} slides`);
    expect(slideCount).toBe(20);

    const cspErrors = errors.filter(e => e.includes('Content Security Policy'));
    expect(cspErrors).toHaveLength(0);
  });

  test('Intro module returns 404', async ({ page }) => {
    const response = await page.goto(`${PROD_URL}/course/cmsc173/module/intro`);
    expect(response.status()).toBe(404);
  });

  test('All other modules still work', async ({ page }) => {
    // Test a few other modules to make sure they still work
    for (const modId of ['01', '05', '12']) {
      const response = await page.goto(`${PROD_URL}/course/cmsc173/module/${modId}`, { waitUntil: 'networkidle' });
      expect(response.status()).toBe(200);

      await page.waitForFunction(() => {
        const counter = document.querySelector('.slide-counter');
        if (!counter) return false;
        const text = counter.textContent || '';
        const match = text.match(/(\d+)/g);
        return match && parseInt(match[match.length - 1]) > 5;
      }, { timeout: 10000 });

      console.log(`Module ${modId}: OK`);
    }
  });
});
