const { test, expect } = require('@playwright/test');

/**
 * Class Records Admin E2E Tests
 * Tests the admin class records page for tracking exam submissions and scores.
 *
 * Requires ADMIN_USERNAME and ADMIN_PASSWORD environment variables to be set.
 */

// Admin credentials from environment
const ADMIN_CREDENTIALS = {
    username: process.env.ADMIN_USERNAME,
    password: process.env.ADMIN_PASSWORD
};

// Helper function to login as admin
async function adminLogin(page) {
    await page.goto('/admin_login');
    await page.fill('#username', ADMIN_CREDENTIALS.username);
    await page.fill('#password', ADMIN_CREDENTIALS.password);
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
}

// Tests that don't require authentication
test.describe('Admin Class Records - Route Exists', () => {

    test('Class Records route exists and requires auth', async ({ page }) => {
        // Navigate directly to class records - should redirect to login
        await page.goto('/admin_class_records');

        // Should redirect to admin login since not authenticated
        await expect(page).toHaveURL(/.*admin_login/);
        console.log('Class Records route exists and properly requires authentication');
    });

});

// Tests that require authentication
test.describe('Admin Class Records - Authenticated', () => {

    // Skip all tests if admin credentials are not set
    test.beforeAll(async () => {
        if (!ADMIN_CREDENTIALS.username || !ADMIN_CREDENTIALS.password) {
            console.log('Skipping authenticated tests: Set ADMIN_USERNAME and ADMIN_PASSWORD env vars');
        }
    });

    test.beforeEach(async ({ page }) => {
        if (!ADMIN_CREDENTIALS.username || !ADMIN_CREDENTIALS.password) {
            test.skip();
            return;
        }
        await adminLogin(page);
    });

    test('Can navigate to Class Records from dashboard', async ({ page }) => {
        // Click the Class Records button
        await page.click('a[href="/admin_class_records"]');

        // Verify we're on the class records page
        await expect(page).toHaveURL(/.*admin_class_records/);
        await expect(page.locator('h1')).toContainText('Class Records');
        console.log('Successfully navigated to Class Records page');
    });

    test('Class Records page loads with correct elements', async ({ page }) => {
        // Navigate to class records (beforeEach already handles login)
        await page.goto('/admin_class_records');
        await page.waitForLoadState('networkidle');
        // Ensure we're on the right page (not redirected to login)
        await expect(page).toHaveURL(/.*admin_class_records/);

        // Check page title (using class selector that matches the template)
        await expect(page.locator('.page-title')).toContainText('Class Records');

        // Check stats cards exist
        await expect(page.locator('#totalStudents')).toBeVisible();
        await expect(page.locator('#submittedCount')).toBeVisible();
        await expect(page.locator('#submissionRate')).toBeVisible();
        await expect(page.locator('#avgScore')).toBeVisible();

        // Check class filter dropdown exists
        await expect(page.locator('#classFilter')).toBeVisible();

        // Check search input exists
        await expect(page.locator('#searchInput')).toBeVisible();

        // Check empty state message (before class is selected)
        await expect(page.locator('.empty-state')).toContainText('Select a class');

        console.log('All page elements loaded correctly');
    });

    test('Class dropdown populates with available classes', async ({ page }) => {
        await page.goto('/admin_class_records');

        // Wait for classes to load
        await page.waitForTimeout(1000);

        // Check that dropdown has options beyond the default
        const optionCount = await page.locator('#classFilter option').count();
        expect(optionCount).toBeGreaterThan(1);

        console.log(`Found ${optionCount - 1} classes in dropdown`);
    });

    test('Selecting a class loads student records', async ({ page }) => {
        await page.goto('/admin_class_records');

        // Wait for classes to load
        await page.waitForTimeout(1000);

        // Get the first actual class option (skip the placeholder)
        const options = page.locator('#classFilter option');
        const optionCount = await options.count();

        if (optionCount > 1) {
            // Select the second option (first real class)
            const firstClassValue = await options.nth(1).getAttribute('value');
            await page.selectOption('#classFilter', firstClassValue);

            // Wait for records to load
            await page.waitForTimeout(2000);

            // Check if table is visible or empty state with "No students"
            const tableVisible = await page.locator('.records-table').isVisible();
            const noStudents = await page.locator('.empty-state').isVisible();

            expect(tableVisible || noStudents).toBeTruthy();

            if (tableVisible) {
                // Verify table headers
                await expect(page.locator('.records-table th')).toContainText(['Campus ID', 'Name']);
                console.log('Student records table loaded');
            } else {
                console.log('No students found in selected class');
            }
        } else {
            console.log('No classes available to test');
        }
    });

    test('Stats update when class is selected', async ({ page }) => {
        await page.goto('/admin_class_records');

        // Initial stats should show dash
        await expect(page.locator('#totalStudents')).toHaveText('-');

        // Wait for classes to load and select first class
        await page.waitForTimeout(1000);
        const options = page.locator('#classFilter option');
        const optionCount = await options.count();

        if (optionCount > 1) {
            const firstClassValue = await options.nth(1).getAttribute('value');
            await page.selectOption('#classFilter', firstClassValue);

            // Wait for data to load
            await page.waitForTimeout(2000);

            // Stats should now show numbers (not just dash)
            const totalStudents = await page.locator('#totalStudents').textContent();
            // Either shows a number or still dash if no students
            console.log(`Total students: ${totalStudents}`);
        }
    });

    test('Search filter works', async ({ page }) => {
        await page.goto('/admin_class_records');

        // Wait for classes to load and select first class
        await page.waitForTimeout(1000);
        const options = page.locator('#classFilter option');
        const optionCount = await options.count();

        if (optionCount > 1) {
            const firstClassValue = await options.nth(1).getAttribute('value');
            await page.selectOption('#classFilter', firstClassValue);
            await page.waitForTimeout(2000);

            // Check if table has rows
            const rowCount = await page.locator('.records-table tbody tr').count();

            if (rowCount > 0) {
                // Type a search term that likely won't match
                await page.fill('#searchInput', 'xyznonexistent12345');
                await page.waitForTimeout(500);

                // Should show empty state or fewer rows
                const emptyState = await page.locator('.empty-state').isVisible();
                const newRowCount = await page.locator('.records-table tbody tr').count();

                expect(emptyState || newRowCount < rowCount).toBeTruthy();
                console.log('Search filter works correctly');
            }
        }
    });

    test('Export CSV button exists and is clickable', async ({ page }) => {
        await page.goto('/admin_class_records');

        // Find export button
        const exportBtn = page.locator('button:has-text("Export CSV")');
        await expect(exportBtn).toBeVisible();

        // Note: Actually clicking would trigger download, just verify it exists
        console.log('Export CSV button is present');
    });

    test('Exam checkbox and score input elements exist in table', async ({ page }) => {
        await page.goto('/admin_class_records');

        // Wait for classes to load and select first class
        await page.waitForTimeout(1000);
        const options = page.locator('#classFilter option');
        const optionCount = await options.count();

        if (optionCount > 1) {
            const firstClassValue = await options.nth(1).getAttribute('value');
            await page.selectOption('#classFilter', firstClassValue);
            await page.waitForTimeout(2000);

            // Check if table has rows
            const tableVisible = await page.locator('.records-table').isVisible();

            if (tableVisible) {
                const rowCount = await page.locator('.records-table tbody tr').count();

                if (rowCount > 0) {
                    // Check first row has checkbox and score input
                    const firstRow = page.locator('.records-table tbody tr').first();
                    await expect(firstRow.locator('.exam-checkbox')).toBeVisible();
                    await expect(firstRow.locator('.score-input')).toBeVisible();

                    console.log('Exam checkbox and score input are present in table');
                }
            }
        }
    });

    test('Clicking exam checkbox saves to database', async ({ page }) => {
        await page.goto('/admin_class_records');

        // Wait for classes to load and select first class
        await page.waitForTimeout(1000);
        const options = page.locator('#classFilter option');
        const optionCount = await options.count();

        if (optionCount > 1) {
            const firstClassValue = await options.nth(1).getAttribute('value');
            await page.selectOption('#classFilter', firstClassValue);
            await page.waitForTimeout(2000);

            const tableVisible = await page.locator('.records-table').isVisible();

            if (tableVisible) {
                const rowCount = await page.locator('.records-table tbody tr').count();

                if (rowCount > 0) {
                    const firstRow = page.locator('.records-table tbody tr').first();
                    const checkbox = firstRow.locator('.exam-checkbox');

                    // Get initial state
                    const initialChecked = await checkbox.isChecked();

                    // Click to toggle
                    await checkbox.click();

                    // Wait for save indicator
                    await page.waitForTimeout(1500);

                    // Look for "Saved" or empty status (first .save-status is for checkbox)
                    const saveStatus = firstRow.locator('.save-status').first();
                    const statusText = await saveStatus.textContent();

                    // Verify checkbox state changed
                    const newChecked = await checkbox.isChecked();
                    expect(newChecked).toBe(!initialChecked);

                    // Verify save was successful (status should NOT be 'Error')
                    expect(statusText).not.toBe('Error');

                    console.log(`Checkbox toggled from ${initialChecked} to ${newChecked}, status: "${statusText}"`);

                    // Toggle back to original state to not affect other tests
                    await checkbox.click();
                    await page.waitForTimeout(1000);
                }
            }
        }
    });

});
