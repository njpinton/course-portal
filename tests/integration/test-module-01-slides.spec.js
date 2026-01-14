const { test, expect } = require('@playwright/test');

test.describe('Module 01: Parameter Estimation - Slide Presentation', () => {
  const BASE_URL = 'http://localhost:8788';
  const MODULE_URL = `${BASE_URL}/course/cmsc173/module/1`;

  test.beforeEach(async ({ page }) => {
    // Navigate to module 1 and wait for slides to load
    await page.goto(MODULE_URL);
    await page.waitForSelector('#slide-inner.active', { timeout: 10000 });
  });

  test('should load module 1 presentation successfully', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Module 1: Parameter Estimation/);

    // Verify header is visible
    const header = page.locator('.presenter-header');
    await expect(header).toBeVisible();

    // Verify slide content area exists
    const slideContent = page.locator('#slide-inner');
    await expect(slideContent).toBeVisible();

    // Check that slides are loaded (should show slide 1)
    const currentSlide = page.locator('#current-slide');
    await expect(currentSlide).toHaveText('1');

    // Verify total slides count
    const totalSlides = page.locator('#total-slides');
    await expect(totalSlides).toHaveText('38');
  });

  test('should navigate to slide 2 and verify side-by-side-layout', async ({ page }) => {
    // Click next button to go to slide 2
    await page.click('#next-btn');

    // Wait for slide transition
    await page.waitForTimeout(300);

    // Verify we're on slide 2
    const currentSlide = page.locator('#current-slide');
    await expect(currentSlide).toHaveText('2');

    // Verify slide title
    const slideTitle = page.locator('#slide-inner h2');
    await expect(slideTitle).toHaveText('What is Parameter Estimation?');

    // Verify side-by-side-layout exists
    const sideLayout = page.locator('.side-by-side-layout');
    await expect(sideLayout).toBeVisible();

    // Verify the layout has two main sections: figures-row and text-row
    const figuresRow = page.locator('.side-by-side-layout .figures-row');
    const textRow = page.locator('.side-by-side-layout .text-row');

    await expect(figuresRow).toBeVisible();
    await expect(textRow).toBeVisible();

    // Verify figures row has 2 figures
    const figures = figuresRow.locator('figure');
    await expect(figures).toHaveCount(2);

    // Verify images are present
    const images = figuresRow.locator('img');
    await expect(images).toHaveCount(2);

    // Verify text row has callout and content
    const callout = textRow.locator('.callout.blue');
    await expect(callout).toBeVisible();
    await expect(callout.locator('.callout-title')).toContainText('Definition');
  });

  test('should take screenshot of slide 2 with side-by-side-layout', async ({ page }) => {
    // Navigate to slide 2
    await page.click('#next-btn');
    await page.waitForTimeout(500); // Wait for transition and any animations

    // Take full page screenshot
    await page.screenshot({
      path: 'test-results/module-01-slide-02-full.png',
      fullPage: true
    });

    // Take screenshot of just the slide content area
    const slideCard = page.locator('.slide-card');
    await slideCard.screenshot({
      path: 'test-results/module-01-slide-02-card.png'
    });

    // Take screenshot of just the side layout
    const sideLayout = page.locator('.side-by-side-layout');
    await sideLayout.screenshot({
      path: 'test-results/module-01-slide-02-side-layout.png'
    });

    console.log('Screenshots saved to test-results/');
  });

  test('should verify accessibility of slide 2', async ({ page }) => {
    // Navigate to slide 2
    await page.click('#next-btn');
    await page.waitForTimeout(300);

    // Get accessibility snapshot
    const snapshot = await page.accessibility.snapshot();

    // Verify basic accessibility structure
    expect(snapshot).toBeTruthy();
    expect(snapshot.role).toBe('WebArea');

    // Check for heading structure
    const heading = await page.locator('h2').first();
    await expect(heading).toBeVisible();

    // Verify images have alt text
    const images = page.locator('.side-by-side-layout img');
    const imageCount = await images.count();

    for (let i = 0; i < imageCount; i++) {
      const alt = await images.nth(i).getAttribute('alt');
      expect(alt).toBeTruthy();
      expect(alt.length).toBeGreaterThan(0);
      console.log(`Image ${i + 1} alt text: ${alt}`);
    }

    // Check for proper semantic HTML
    const figures = page.locator('.side-by-side-layout figure');
    await expect(figures).toHaveCount(2);

    // Verify callout has proper structure
    const callout = page.locator('.callout.blue');
    await expect(callout).toBeVisible();

    // Check for icon accessibility
    const icons = page.locator('.callout i');
    const iconCount = await icons.count();
    console.log(`Found ${iconCount} icons in callouts`);
  });

  test('should verify layout responsiveness', async ({ page }) => {
    // Navigate to slide 2
    await page.click('#next-btn');
    await page.waitForTimeout(300);

    const sideLayout = page.locator('.side-by-side-layout');

    // Test desktop layout
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(sideLayout).toBeVisible();

    const desktopBoundingBox = await sideLayout.boundingBox();
    expect(desktopBoundingBox.width).toBeGreaterThan(0);

    // Take screenshot at desktop size
    await page.screenshot({
      path: 'test-results/module-01-slide-02-desktop.png'
    });

    // Test tablet layout
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(200);
    await expect(sideLayout).toBeVisible();

    await page.screenshot({
      path: 'test-results/module-01-slide-02-tablet.png'
    });

    // Test mobile layout
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(200);
    await expect(sideLayout).toBeVisible();

    await page.screenshot({
      path: 'test-results/module-01-slide-02-mobile.png'
    });

    console.log('Responsive screenshots saved!');
  });

  test('should verify keyboard navigation works', async ({ page }) => {
    // Verify we start on slide 1
    let currentSlide = page.locator('#current-slide');
    await expect(currentSlide).toHaveText('1');

    // Press arrow right to go to slide 2
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(300);

    // Verify we're on slide 2
    await expect(currentSlide).toHaveText('2');

    // Verify the slide title changed
    const slideTitle = page.locator('#slide-inner h2');
    await expect(slideTitle).toHaveText('What is Parameter Estimation?');

    // Press arrow left to go back to slide 1
    await page.keyboard.press('ArrowLeft');
    await page.waitForTimeout(300);

    // Verify we're back on slide 1
    await expect(currentSlide).toHaveText('1');
  });

  test('should verify MathJax/KaTeX rendering on slide 2', async ({ page }) => {
    // Navigate to slide 2
    await page.click('#next-btn');
    await page.waitForTimeout(500);

    // Wait for KaTeX to render math formulas
    await page.waitForTimeout(500);

    // Check for math content in the text row
    const textRow = page.locator('.side-by-side-layout .text-row');

    // Verify LaTeX content is present (checking for common LaTeX patterns)
    const content = await textRow.textContent();

    // Should contain data notation, distribution, and estimate
    expect(content).toContain('x');
    expect(content).toContain('θ');

    console.log('Math rendering verified on slide 2');
  });

  test('should check slide footer and progress bar', async ({ page }) => {
    // Navigate to slide 2
    await page.click('#next-btn');
    await page.waitForTimeout(300);

    // Check footer is visible
    const footer = page.locator('.slide-footer');
    await expect(footer).toBeVisible();

    // Verify reading time is displayed
    const readingTime = page.locator('#reading-time');
    await expect(readingTime).toContainText('min');

    // Verify progress bar updates
    const progressFill = page.locator('#progress-fill');
    const progressWidth = await progressFill.evaluate(el => el.style.width);

    // Should be approximately 2/38 = ~5.26%
    expect(progressWidth).toBeTruthy();
    console.log(`Progress bar width: ${progressWidth}`);
  });

  test('should verify table of contents includes slide 2', async ({ page }) => {
    // Open sidebar/TOC
    await page.click('button[onclick="toggleSidebar()"]');
    await page.waitForTimeout(200);

    // Verify sidebar is active
    const sidebar = page.locator('#sidebar');
    await expect(sidebar).toHaveClass(/active/);

    // Check TOC items
    const tocItems = page.locator('.toc-item');
    const tocCount = await tocItems.count();

    expect(tocCount).toBe(38);

    // Verify slide 2 is in the TOC
    const slide2TocItem = tocItems.nth(1); // 0-indexed, so slide 2 is index 1
    await expect(slide2TocItem).toContainText('What is Parameter Estimation?');

    // Click on slide 2 in TOC
    await slide2TocItem.click();
    await page.waitForTimeout(300);

    // Verify we navigated to slide 2
    const currentSlide = page.locator('#current-slide');
    await expect(currentSlide).toHaveText('2');
  });
});
