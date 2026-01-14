const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8788';

test.describe('Combined Module 0 Tests', () => {
  test('Module 0 loads with all slides', async ({ page }) => {
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.goto(`${BASE_URL}/course/cmsc173/module/00`, { waitUntil: 'networkidle' });

    // Wait for slides to load
    await page.waitForFunction(() => {
      const counter = document.querySelector('.slide-counter');
      if (!counter) return false;
      const text = counter.textContent || '';
      const match = text.match(/(\d+)/g);
      if (!match) return false;
      return parseInt(match[match.length - 1]) > 15;
    }, { timeout: 10000 });

    // Get slide count
    const slideCount = await page.evaluate(() => {
      const counter = document.querySelector('.slide-counter');
      if (!counter) return 0;
      const text = counter.textContent || '';
      const match = text.match(/(\d+)/g);
      return match ? parseInt(match[match.length - 1]) : 0;
    });

    console.log(`Combined Module 0: ${slideCount} slides`);

    // Should have ~20 slides (combined from intro + module 0)
    expect(slideCount).toBeGreaterThanOrEqual(18);

    // Check no CSP errors
    const cspErrors = errors.filter(e => e.includes('Content Security Policy'));
    expect(cspErrors).toHaveLength(0);

    // Verify title
    const title = await page.locator('h1').textContent();
    expect(title).toContain('Module 0');
  });

  test('Intro module returns 404', async ({ page }) => {
    const response = await page.goto(`${BASE_URL}/course/cmsc173/module/intro`);
    expect(response.status()).toBe(404);
  });

  test('Navigation works through all slides', async ({ page }) => {
    await page.goto(`${BASE_URL}/course/cmsc173/module/00`, { waitUntil: 'networkidle' });

    // Wait for slides to load
    await page.waitForFunction(() => {
      const counter = document.querySelector('.slide-counter');
      return counter && counter.textContent.includes('/');
    });

    // Navigate to next slide
    await page.click('.nav-next .nav-btn');
    await page.waitForTimeout(500);

    const currentSlide = await page.evaluate(() => {
      return document.getElementById('current-slide')?.textContent;
    });

    expect(currentSlide).toBe('2');
  });
});
