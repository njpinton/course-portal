const { chromium } = require('@playwright/test');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto('http://localhost:8788/course/cmsc173/module/1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(1500);

    // Check if the CSS rule exists
    const cssRuleExists = await page.evaluate(() => {
      const sheets = Array.from(document.styleSheets);
      let found = false;
      let ruleText = '';

      for (const sheet of sheets) {
        try {
          const rules = Array.from(sheet.cssRules || sheet.rules || []);
          for (const rule of rules) {
            if (rule.selectorText === '.stacked-figures-layout') {
              found = true;
              ruleText = rule.cssText;
              break;
            }
          }
          if (found) break;
        } catch (e) {
          // Skip CORS-protected stylesheets
        }
      }

      return { found, ruleText };
    });

    console.log('CSS Rule check:', cssRuleExists);

    // Check what styles are actually applied
    const appliedStyles = await page.evaluate(() => {
      const el = document.querySelector('.stacked-figures-layout');
      if (!el) return { error: 'Element not found' };

      const computed = window.getComputedStyle(el);
      const inline = el.style;

      return {
        className: el.className,
        computedDisplay: computed.display,
        computedGridTemplateColumns: computed.gridTemplateColumns,
        computedGap: computed.gap,
        inlineStyles: el.getAttribute('style'),
        allComputedStyles: {
          display: computed.display,
          gridTemplateColumns: computed.gridTemplateColumns,
          gridTemplateRows: computed.gridTemplateRows,
          gap: computed.gap,
          height: computed.height,
          minHeight: computed.minHeight
        }
      };
    });

    console.log('\nApplied styles:', JSON.stringify(appliedStyles, null, 2));

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
})();
