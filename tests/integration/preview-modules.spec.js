const { test, expect } = require('@playwright/test');

const PREVIEW_URL = 'https://presenter-67wb5j4w0-noels-projects-6ddd7b58.vercel.app';

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

test.describe('Preview Module Tests', () => {
  for (const mod of modules) {
    test(`Module ${mod.id} (${mod.name}) loads correctly`, async ({ page }) => {
      const url = `${PREVIEW_URL}/course/cmsc173/module/${mod.id}`;

      // Capture console errors
      const errors = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      await page.goto(url, { waitUntil: 'networkidle' });

      // Wait for slides to load
      await page.waitForFunction(() => {
        const counter = document.getElementById('total-slides') ||
                        document.querySelector('.slide-counter');
        if (!counter) return false;
        const text = counter.textContent || '';
        const match = text.match(/(\d+)/g);
        if (!match) return false;
        const total = parseInt(match[match.length - 1]);
        return total > 1;
      }, { timeout: 15000 });

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

      // Check no CSP errors
      const cspErrors = errors.filter(e => e.includes('Content Security Policy'));
      expect(cspErrors).toHaveLength(0);

      expect(slideCount).toBeGreaterThan(0);
    });
  }
});
