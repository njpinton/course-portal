const { chromium } = require('@playwright/test');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('1. Navigating to module 1...');
    await page.goto('http://localhost:8788/course/cmsc173/module/1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    console.log('2. Going to slide 2...');
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(1500);

    console.log('\n3. Inspecting stacked-figures-layout element...');
    const stackedLayout = page.locator('.stacked-figures-layout').first();

    if (await stackedLayout.count() > 0) {
      // Get computed styles and dimensions
      const layoutInfo = await stackedLayout.evaluate((el) => {
        const styles = window.getComputedStyle(el);
        return {
          display: styles.display,
          gridTemplateColumns: styles.gridTemplateColumns,
          gap: styles.gap,
          height: styles.height,
          minHeight: styles.minHeight,
          boundingBox: el.getBoundingClientRect()
        };
      });

      console.log('Layout element info:');
      console.log(JSON.stringify(layoutInfo, null, 2));

      // Check figures column
      const figuresColumn = page.locator('.stacked-figures-layout .figures-column').first();
      if (await figuresColumn.count() > 0) {
        const figuresInfo = await figuresColumn.evaluate((el) => {
          const styles = window.getComputedStyle(el);
          const figures = el.querySelectorAll('figure');
          return {
            display: styles.display,
            flexDirection: styles.flexDirection,
            gap: styles.gap,
            height: styles.height,
            boundingBox: el.getBoundingClientRect(),
            figureCount: figures.length,
            figuresInfo: Array.from(figures).map((fig, i) => {
              const img = fig.querySelector('img');
              const figStyles = window.getComputedStyle(fig);
              return {
                index: i,
                flex: figStyles.flex,
                height: figStyles.height,
                boundingBox: fig.getBoundingClientRect(),
                img: img ? {
                  src: img.src.split('/').slice(-1)[0],
                  naturalWidth: img.naturalWidth,
                  naturalHeight: img.naturalHeight,
                  displayWidth: img.width,
                  displayHeight: img.height,
                  maxHeight: window.getComputedStyle(img).maxHeight
                } : null
              };
            })
          };
        });

        console.log('\nFigures column info:');
        console.log(JSON.stringify(figuresInfo, null, 2));
      }

      // Check text column
      const textColumn = page.locator('.stacked-figures-layout .text-column').first();
      if (await textColumn.count() > 0) {
        const textInfo = await textColumn.evaluate((el) => {
          const styles = window.getComputedStyle(el);
          return {
            display: styles.display,
            flexDirection: styles.flexDirection,
            justifyContent: styles.justifyContent,
            height: styles.height,
            boundingBox: el.getBoundingClientRect()
          };
        });

        console.log('\nText column info:');
        console.log(JSON.stringify(textInfo, null, 2));
      }

      // Take screenshots
      console.log('\n4. Taking screenshots...');
      await stackedLayout.screenshot({
        path: '/Users/njpinton/projects/git/presenter_app/test-results/stacked-layout-debug.png'
      });

      await page.screenshot({
        path: '/Users/njpinton/projects/git/presenter_app/test-results/full-page-debug.png',
        fullPage: true
      });

      console.log('Screenshots saved!');
    } else {
      console.log('ERROR: .stacked-figures-layout not found');
    }

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
})();
