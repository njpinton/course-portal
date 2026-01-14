const { test, expect } = require('@playwright/test');

/**
 * Module 1 Slide Review Script
 * This script navigates through each slide in Module 1 and captures screenshots
 * for design review based on the slide-presenter skill guidelines.
 */

test.describe('Module 1: Parameter Estimation - Slide Review', () => {
  test.setTimeout(300000); // 5 minutes timeout for full review

  test('Review all slides and capture screenshots', async ({ page }) => {
    // Navigate to Module 1 presentation
    await page.goto('/course/cmsc173/module/1');

    // Wait for slides to load
    await page.waitForSelector('.slide-inner.active', { timeout: 10000 });

    // Get total number of slides
    const totalSlides = await page.locator('#total-slides').textContent();
    const slideCount = parseInt(totalSlides);

    console.log(`\n${'='.repeat(80)}`);
    console.log(`MODULE 1: PARAMETER ESTIMATION - SLIDE REVIEW`);
    console.log(`Total Slides: ${slideCount}`);
    console.log(`${'='.repeat(80)}\n`);

    // Review each slide
    for (let i = 0; i < slideCount; i++) {
      // Get slide info
      const title = await page.locator('.slide-inner h2').textContent();
      const currentSlide = i + 1;

      console.log(`\n--- SLIDE ${currentSlide}/${slideCount}: "${title}" ---`);

      // Take screenshot
      const screenshotPath = `slide-reviews/module-01/slide-${String(currentSlide).padStart(2, '0')}.png`;
      await page.screenshot({
        path: screenshotPath,
        fullPage: false
      });

      // Check for scrolling issues (content overflow)
      const slideContent = page.locator('.slide-content');
      const scrollHeight = await slideContent.evaluate(el => el.scrollHeight);
      const clientHeight = await slideContent.evaluate(el => el.clientHeight);
      const hasOverflow = scrollHeight > clientHeight + 10; // 10px tolerance

      if (hasOverflow) {
        console.log(`  ⚠️  OVERFLOW: Content requires scrolling (${scrollHeight}px > ${clientHeight}px)`);
      } else {
        console.log(`  ✓  No scrolling required`);
      }

      // Check title length
      const titleLength = title.length;
      if (titleLength > 40) {
        console.log(`  ⚠️  TITLE TOO LONG: ${titleLength} chars (max 40)`);
      }

      // Check for images
      const images = await page.locator('.slide-inner img').count();
      if (images > 0) {
        console.log(`  📷 Images: ${images}`);

        // Check for broken images
        const brokenImages = await page.locator('.slide-inner img').evaluateAll(imgs =>
          imgs.filter(img => !img.complete || img.naturalWidth === 0).length
        );
        if (brokenImages > 0) {
          console.log(`  ❌ BROKEN IMAGES: ${brokenImages}`);
        }
      }

      // Check for code blocks
      const codeBlocks = await page.locator('.code-block').count();
      if (codeBlocks > 0) {
        console.log(`  💻 Code blocks: ${codeBlocks}`);
      }

      // Check for callouts
      const callouts = await page.locator('.callout').count();
      if (callouts > 0) {
        console.log(`  📌 Callouts: ${callouts}`);
      }

      // Check for cards
      const cards = await page.locator('.info-card').count();
      if (cards > 0) {
        console.log(`  🗂️  Cards: ${cards}`);
        if (cards > 4) {
          console.log(`  ⚠️  TOO MANY CARDS: ${cards} (max 4)`);
        }
      }

      // Check for bullet points
      const bullets = await page.locator('.slide-inner li').count();
      if (bullets > 5) {
        console.log(`  ⚠️  TOO MANY BULLETS: ${bullets} (max 5)`);
      }

      // Check for math content
      const mathContent = await page.locator('.katex').count();
      if (mathContent > 0) {
        console.log(`  📐 Math elements: ${mathContent}`);
      }

      // Check stacked figures layout
      const stackedLayout = await page.locator('.stacked-figures-layout').count();
      if (stackedLayout > 0) {
        console.log(`  📊 Stacked figures layout`);
      }

      // Navigate to next slide (unless on last slide)
      if (i < slideCount - 1) {
        await page.keyboard.press('ArrowRight');
        await page.waitForTimeout(200); // Wait for animation
      }
    }

    console.log(`\n${'='.repeat(80)}`);
    console.log(`REVIEW COMPLETE`);
    console.log(`Screenshots saved to: slide-reviews/module-01/`);
    console.log(`${'='.repeat(80)}\n`);
  });
});
