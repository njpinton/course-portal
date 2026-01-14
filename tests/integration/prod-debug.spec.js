const { test, expect } = require('@playwright/test');

const PROD_URL = 'https://presenterapp-nine.vercel.app';

test('Debug Module 02 - Linear Regression', async ({ page }) => {
  const consoleMessages = [];
  const networkErrors = [];

  // Capture console messages
  page.on('console', msg => {
    consoleMessages.push({ type: msg.type(), text: msg.text() });
  });

  // Capture network failures
  page.on('requestfailed', request => {
    networkErrors.push({
      url: request.url(),
      failure: request.failure()?.errorText
    });
  });

  // Capture response errors
  page.on('response', response => {
    if (!response.ok()) {
      networkErrors.push({
        url: response.url(),
        status: response.status(),
        statusText: response.statusText()
      });
    }
  });

  const url = `${PROD_URL}/course/cmsc173/module/02`;
  console.log(`Testing: ${url}`);

  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

  // Wait a bit for any async operations
  await page.waitForTimeout(3000);

  // Log any console errors
  console.log('\n=== Console Messages ===');
  for (const msg of consoleMessages) {
    console.log(`[${msg.type}] ${msg.text}`);
  }

  // Log network errors
  console.log('\n=== Network Errors ===');
  for (const err of networkErrors) {
    console.log(JSON.stringify(err));
  }

  // Get current state
  const pageState = await page.evaluate(() => {
    return {
      slideCounter: document.querySelector('.slide-counter')?.textContent ||
                    document.getElementById('total-slides')?.textContent || 'not found',
      hasError: document.body.innerHTML.includes('Failed to load'),
      slidesArrayLength: typeof slides !== 'undefined' ? slides.length : 'undefined',
      bodyText: document.body.innerText.substring(0, 500)
    };
  });

  console.log('\n=== Page State ===');
  console.log(JSON.stringify(pageState, null, 2));

  // Check JSON directly
  const jsonResponse = await page.evaluate(async () => {
    try {
      const resp = await fetch('/static/data/courses/cmsc173/module-02-slides.json');
      const data = await resp.json();
      return { ok: true, slideCount: data.slides?.length, title: data.title };
    } catch (e) {
      return { ok: false, error: e.message };
    }
  });

  console.log('\n=== Direct JSON Fetch ===');
  console.log(JSON.stringify(jsonResponse, null, 2));
});
