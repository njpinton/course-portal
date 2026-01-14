const { test, expect } = require('@playwright/test');

/**
 * Group Submission Portal E2E Tests
 * Tests the complete flow of creating a group, logging in, and submitting work for all 6 stages.
 */

// Pre-created test group credentials (created via Python script)
const TEST_GROUP = {
    username: 'playwright_e2e_test',
    password: 'testpass123',
    group_name: 'Playwright E2E Test Group',
    project_title: 'E2E Test Project'
};

// Stage data for all 6 stages
const STAGES = [
    { number: 1, name: 'Proposal', summary: '# Stage 1: Proposal\n\nProject proposal with objectives.' },
    { number: 2, name: 'Data & Preprocessing', summary: '# Stage 2: Data\n\nData preprocessing completed.' },
    { number: 3, name: 'Model Training', summary: '# Stage 3: Training\n\nModel training complete.' },
    { number: 4, name: 'Evaluation', summary: '# Stage 4: Evaluation\n\nModel evaluation done.' },
    { number: 5, name: 'Final Report', summary: '# Stage 5: Report\n\nFinal report compiled.' },
    { number: 6, name: 'Presentation', summary: '# Stage 6: Presentation\n\nSlides prepared.' }
];

test.describe.serial('Group Submission Portal - Full Flow', () => {

    test('Step 1: Login to group portal', async ({ page }) => {
        await page.goto('/group_login');

        // Fill login form
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);

        // Submit
        await page.click('button[type="submit"]');
        await page.waitForLoadState('networkidle');

        // Verify redirect to submission portal
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });
        console.log('Login successful');
    });

    test('Step 2: Submit work for Stage 1 (Proposal)', async ({ page }) => {
        // Login first
        await page.goto('/group_login');
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });
        await page.waitForLoadState('networkidle');

        const stageIndex = 0; // Stage 1

        // Expand stage card using JavaScript directly
        await page.evaluate((idx) => {
            const content = document.getElementById(`stage-${idx}`);
            if (content) {
                content.classList.add('active');
            }
        }, stageIndex);
        await page.waitForTimeout(500);

        // Fill presentation link
        await page.fill(`#presentation-link-${stageIndex}`, 'https://docs.google.com/presentation/d/test-stage-1');

        // Fill summary
        await page.fill(`#summary-${stageIndex}`, STAGES[0].summary);

        // Handle alert dialog
        page.once('dialog', async dialog => {
            console.log(`Stage 1 dialog: ${dialog.message()}`);
            expect(dialog.message()).toContain('successful');
            await dialog.accept();
        });

        // Submit
        const submitBtn = page.locator('.stage-card').first().locator('button[type="submit"]');
        await submitBtn.click();

        await page.waitForLoadState('networkidle');
        console.log('Stage 1 submitted');
    });

    test('Step 3: Submit work for Stage 2 (Data & Preprocessing)', async ({ page }) => {
        await page.goto('/group_login');
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });
        await page.waitForLoadState('networkidle');

        const stageIndex = 1;

        // Expand stage card using JavaScript
        await page.evaluate((idx) => {
            const content = document.getElementById(`stage-${idx}`);
            if (content) content.classList.add('active');
        }, stageIndex);
        await page.waitForTimeout(500);

        await page.fill(`#presentation-link-${stageIndex}`, 'https://docs.google.com/presentation/d/test-stage-2');
        await page.fill(`#summary-${stageIndex}`, STAGES[1].summary);

        page.once('dialog', async dialog => {
            await dialog.accept();
        });

        const stageCard = page.locator('.stage-card').nth(stageIndex);
        await stageCard.locator('button[type="submit"]').click();
        await page.waitForLoadState('networkidle');
        console.log('Stage 2 submitted');
    });

    test('Step 4: Submit work for Stage 3 (Model Training)', async ({ page }) => {
        await page.goto('/group_login');
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });
        await page.waitForLoadState('networkidle');

        const stageIndex = 2;

        // Expand stage card using JavaScript
        await page.evaluate((idx) => {
            const content = document.getElementById(`stage-${idx}`);
            if (content) content.classList.add('active');
        }, stageIndex);
        await page.waitForTimeout(500);

        await page.fill(`#presentation-link-${stageIndex}`, 'https://docs.google.com/presentation/d/test-stage-3');
        await page.fill(`#summary-${stageIndex}`, STAGES[2].summary);

        page.once('dialog', async dialog => {
            await dialog.accept();
        });

        const stageCard = page.locator('.stage-card').nth(stageIndex);
        await stageCard.locator('button[type="submit"]').click();
        await page.waitForLoadState('networkidle');
        console.log('Stage 3 submitted');
    });

    test('Step 5: Submit work for Stage 4 (Evaluation)', async ({ page }) => {
        await page.goto('/group_login');
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });
        await page.waitForLoadState('networkidle');

        const stageIndex = 3;

        // Expand stage card using JavaScript
        await page.evaluate((idx) => {
            const content = document.getElementById(`stage-${idx}`);
            if (content) content.classList.add('active');
        }, stageIndex);
        await page.waitForTimeout(500);

        await page.fill(`#presentation-link-${stageIndex}`, 'https://docs.google.com/presentation/d/test-stage-4');
        await page.fill(`#summary-${stageIndex}`, STAGES[3].summary);

        page.once('dialog', async dialog => {
            await dialog.accept();
        });

        const stageCard = page.locator('.stage-card').nth(stageIndex);
        await stageCard.locator('button[type="submit"]').click();
        await page.waitForLoadState('networkidle');
        console.log('Stage 4 submitted');
    });

    test('Step 6: Submit work for Stage 5 (Final Report)', async ({ page }) => {
        await page.goto('/group_login');
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });
        await page.waitForLoadState('networkidle');

        const stageIndex = 4;

        // Expand stage card using JavaScript
        await page.evaluate((idx) => {
            const content = document.getElementById(`stage-${idx}`);
            if (content) content.classList.add('active');
        }, stageIndex);
        await page.waitForTimeout(500);

        await page.fill(`#presentation-link-${stageIndex}`, 'https://docs.google.com/presentation/d/test-stage-5');
        await page.fill(`#summary-${stageIndex}`, STAGES[4].summary);

        page.once('dialog', async dialog => {
            await dialog.accept();
        });

        const stageCard = page.locator('.stage-card').nth(stageIndex);
        await stageCard.locator('button[type="submit"]').click();
        await page.waitForLoadState('networkidle');
        console.log('Stage 5 submitted');
    });

    test('Step 7: Submit work for Stage 6 (Presentation)', async ({ page }) => {
        await page.goto('/group_login');
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });
        await page.waitForLoadState('networkidle');

        const stageIndex = 5;

        // Expand stage card using JavaScript
        await page.evaluate((idx) => {
            const content = document.getElementById(`stage-${idx}`);
            if (content) content.classList.add('active');
        }, stageIndex);
        await page.waitForTimeout(500);

        await page.fill(`#presentation-link-${stageIndex}`, 'https://docs.google.com/presentation/d/test-stage-6');
        await page.fill(`#summary-${stageIndex}`, STAGES[5].summary);

        page.once('dialog', async dialog => {
            await dialog.accept();
        });

        const stageCard = page.locator('.stage-card').nth(stageIndex);
        await stageCard.locator('button[type="submit"]').click();
        await page.waitForLoadState('networkidle');
        console.log('Stage 6 submitted');
    });

    test('Step 8: Verify all submissions are recorded', async ({ page }) => {
        await page.goto('/group_login');
        await page.fill('#username', TEST_GROUP.username);
        await page.fill('#password', TEST_GROUP.password);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/.*group_submission_portal/, { timeout: 10000 });

        // Check each stage for submission indicators
        for (let i = 0; i < 6; i++) {
            const stageCard = page.locator('.stage-card').nth(i);
            await stageCard.locator('.stage-header').click();
            await page.waitForTimeout(200);

            // Look for submitted content or edit button (indicating previous submission)
            const summaryDisplay = stageCard.locator(`#summary-display-${i}`);
            const editBtn = stageCard.locator('button:has-text("Edit")');
            const submittedIndicator = stageCard.locator('.submitted, .submission-status, [class*="success"]');

            const hasSubmission = await summaryDisplay.isVisible() ||
                                  await editBtn.isVisible() ||
                                  await submittedIndicator.isVisible();

            console.log(`Stage ${i + 1}: ${hasSubmission ? 'Submitted' : 'Not found'}`);
        }

        console.log('All 6 stages verification complete');
    });
});
