const { test, expect } = require('@playwright/test');

const PROD_URL = 'https://presenterapp-nine.vercel.app';

const modules = [
  { id: 'intro', name: 'Welcome/Intro' },
  { id: '00', name: 'Introduction to ML' },
  { id: '01', name: 'Parameter Estimation' },
  { id: '02', name: 'Linear Regression' },
  { id: '03', name: 'Regularization' },
  { id: '04', name: 'EDA' },
  { id: '05', name: 'Model Selection' },
  { id: '06', name: 'Cross Validation' },
  { id: '07', name: 'PCA' },
  { id: '08', name: 'Logistic Regression' },
  { id: '09', name: 'Classification' },
  { id: '10', name: 'Kernel Methods' },
  { id: '11', name: 'Clustering' },
  { id: '12', name: 'Neural Networks' },
  { id: '13', name: 'Advanced NN' },
];

test.describe('Production Module Tests', () => {
  for (const mod of modules) {
    test(`Module ${mod.id} (${mod.name}) loads correctly`, async ({ page }) => {
      const url = `${PROD_URL}/course/cmsc173/module/${mod.id}`;

      await page.goto(url, { waitUntil: 'networkidle' });

      // Wait for slides to load (either inline or via JSON)
      // Note: intro module only has 1 slide, other modules have multiple
      const minSlides = mod.id === 'intro' ? 1 : 2;
      await page.waitForFunction((min) => {
        const counter = document.getElementById('total-slides') ||
                        document.querySelector('.slide-counter');
        if (!counter) return false;
        const text = counter.textContent || '';
        const match = text.match(/(\d+)/);
        return match && parseInt(match[0]) >= min;
      }, minSlides, { timeout: 10000 });

      // Get slide count
      const slideCount = await page.evaluate(() => {
        const counter = document.getElementById('total-slides') ||
                        document.querySelector('.slide-counter');
        if (!counter) return 0;
        const text = counter.textContent || '';
        const match = text.match(/(\d+)/g);
        return match ? parseInt(match[match.length - 1]) : 0;
      });

      console.log(`Module ${mod.id}: ${slideCount} slides`);
      expect(slideCount).toBeGreaterThan(0);

      // Check no error message is visible
      const errorVisible = await page.locator('text=Failed to load').isVisible().catch(() => false);
      expect(errorVisible).toBe(false);
    });
  }
});
