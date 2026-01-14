const { test, expect } = require('@playwright/test');

const PROD_URL = 'https://presenterapp-nine.vercel.app';

test.describe('Final Module 0 Check', () => {
  test('Module 0 renders slide titles correctly', async ({ page }) => {
    await page.goto(`${PROD_URL}/course/cmsc173/module/00`, { waitUntil: 'networkidle' });

    // Wait for slide to render
    await page.waitForTimeout(2000);

    // Check that title is NOT showing ${slide.title}
    const titleText = await page.locator('h2').first().textContent();
    console.log(`Title: ${titleText}`);

    expect(titleText).not.toContain('${');
    expect(titleText).toBe('Welcome to CMSC 173');
  });

  test('Burger menu works', async ({ page }) => {
    await page.goto(`${PROD_URL}/course/cmsc173/module/00`, { waitUntil: 'networkidle' });

    // Wait for page to load
    await page.waitForTimeout(1000);

    // Click burger menu
    await page.click('.icon-btn[title="Menu"]');
    await page.waitForTimeout(500);

    // Check dropdown is visible
    const dropdown = page.locator('#dropdown-menu');
    const isVisible = await dropdown.evaluate(el => {
      const style = window.getComputedStyle(el);
      return style.opacity === '1' && style.visibility === 'visible';
    });

    console.log(`Dropdown visible: ${isVisible}`);
    expect(isVisible).toBe(true);

    // Check Home link is visible
    const homeLink = page.locator('.menu-item:has-text("Home")');
    await expect(homeLink).toBeVisible();
  });

  test('Navigation to other modules works', async ({ page }) => {
    await page.goto(`${PROD_URL}/course/cmsc173/module/00`, { waitUntil: 'networkidle' });

    // Navigate to next slide
    await page.click('.nav-next .nav-btn');
    await page.waitForTimeout(500);

    const slideNum = await page.locator('#current-slide').textContent();
    expect(slideNum).toBe('2');

    // Check second slide title
    const titleText = await page.locator('h2').first().textContent();
    console.log(`Slide 2 title: ${titleText}`);
    expect(titleText).toBe('What is Machine Learning?');
  });
});
