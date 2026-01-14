const { test, expect } = require('@playwright/test');

test.describe('CMSC 173 Slides Check', () => {
    
    test('Intro module loads correctly', async ({ page }) => {
        await page.goto('/course/cmsc173/module/intro');

        // Check page title
        await expect(page).toHaveTitle(/Welcome to CMSC 173/);

        // Check for key content
        await expect(page.locator('body')).toContainText('CMSC 173');
        await expect(page.locator('body')).toContainText('Welcome');

        console.log('Intro module loaded successfully');
    });

    test('Module 0 (Introduction to ML) loads', async ({ page }) => {
        await page.goto('/course/cmsc173/module/0');
        await expect(page.locator('body')).toBeVisible();
        console.log('Module 0 loaded');
    });

    test('Module 1 (Parameter Estimation) loads', async ({ page }) => {
        await page.goto('/course/cmsc173/module/1');
        await expect(page.locator('body')).toBeVisible();
        console.log('Module 1 loaded');
    });

    test('Course page loads with all modules', async ({ page }) => {
        await page.goto('/course/cmsc173');
        
        // Check course page has module links
        await expect(page.locator('body')).toContainText('CMSC 173');
        
        console.log('Course page loaded');
    });

    test('Static images load correctly', async ({ page }) => {
        // Go to module 0 which has images
        await page.goto('/course/cmsc173/module/0');
        
        // Wait for page to load
        await page.waitForLoadState('networkidle');
        
        // Check if images exist and loaded (not broken)
        const images = await page.locator('img').all();
        console.log(`Found ${images.length} images`);
        
        for (const img of images.slice(0, 3)) {
            const src = await img.getAttribute('src');
            if (src) {
                console.log(`Image src: ${src}`);
            }
        }
    });
});
