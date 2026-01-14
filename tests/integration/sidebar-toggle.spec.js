/**
 * Playwright tests for sidebar toggle button functionality
 * Tests the collapsible sidebar on desktop view
 */
const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://127.0.0.1:8788';

test.describe('Sidebar Toggle Button', () => {
    test.beforeEach(async ({ page }) => {
        // Set desktop viewport
        await page.setViewportSize({ width: 1280, height: 800 });
        await page.goto(BASE_URL);
        // Wait for sidebar to be visible
        await page.waitForSelector('#sidebar');
    });

    test('toggle button is visible on desktop', async ({ page }) => {
        const toggleButton = page.locator('#sidebar-toggle');

        // Button should be visible on desktop
        await expect(toggleButton).toBeVisible();

        // Button should have correct aria-label
        await expect(toggleButton).toHaveAttribute('aria-label', 'Toggle sidebar');
    });

    test('toggle button is hidden on mobile', async ({ page }) => {
        // Set mobile viewport
        await page.setViewportSize({ width: 375, height: 667 });
        await page.reload();

        const toggleButton = page.locator('#sidebar-toggle');

        // Button should be hidden on mobile
        await expect(toggleButton).toBeHidden();
    });

    test('clicking toggle collapses sidebar to icons only', async ({ page }) => {
        const sidebar = page.locator('#sidebar');
        const toggleButton = page.locator('#sidebar-toggle');

        // Initially sidebar should NOT be collapsed
        await expect(sidebar).not.toHaveClass(/collapsed/);

        // Get initial sidebar width
        const initialWidth = await sidebar.evaluate(el => el.offsetWidth);
        expect(initialWidth).toBe(260); // Default sidebar width

        // Click toggle button
        await toggleButton.click();

        // Move mouse away from sidebar to avoid hover expansion
        await page.mouse.move(500, 300);

        // Wait for transition
        await page.waitForTimeout(200);

        // Sidebar should now have collapsed class
        await expect(sidebar).toHaveClass(/collapsed/);

        // Sidebar should be narrower (68px when collapsed)
        const collapsedWidth = await sidebar.evaluate(el => el.offsetWidth);
        expect(collapsedWidth).toBe(68);

        // Nav item text should be hidden
        const navItemText = page.locator('.nav-item span:not(.nav-item-icon)').first();
        await expect(navItemText).toBeHidden();
    });

    test('clicking toggle again expands sidebar', async ({ page }) => {
        const sidebar = page.locator('#sidebar');
        const toggleButton = page.locator('#sidebar-toggle');

        // First collapse
        await toggleButton.click();
        await page.waitForTimeout(200);
        await expect(sidebar).toHaveClass(/collapsed/);

        // Click again to expand
        await toggleButton.click();
        await page.waitForTimeout(200);

        // Sidebar should NOT be collapsed
        await expect(sidebar).not.toHaveClass(/collapsed/);

        // Width should be back to normal
        const expandedWidth = await sidebar.evaluate(el => el.offsetWidth);
        expect(expandedWidth).toBe(260);

        // Nav item text should be visible again
        const navItemText = page.locator('.nav-item span:not(.nav-item-icon)').first();
        await expect(navItemText).toBeVisible();
    });

    test('collapsed state persists in localStorage', async ({ page }) => {
        const toggleButton = page.locator('#sidebar-toggle');

        // Collapse sidebar
        await toggleButton.click();
        await page.waitForTimeout(200);

        // Check localStorage
        const isCollapsed = await page.evaluate(() => {
            return localStorage.getItem('sidebarCollapsed');
        });
        expect(isCollapsed).toBe('true');

        // Expand sidebar
        await toggleButton.click();
        await page.waitForTimeout(200);

        // Check localStorage again
        const isExpanded = await page.evaluate(() => {
            return localStorage.getItem('sidebarCollapsed');
        });
        expect(isExpanded).toBe('false');
    });

    test('sidebar expands on hover when collapsed', async ({ page }) => {
        const sidebar = page.locator('#sidebar');
        const toggleButton = page.locator('#sidebar-toggle');

        // Collapse sidebar
        await toggleButton.click();
        await page.waitForTimeout(200);

        // Hover over sidebar
        await sidebar.hover();
        await page.waitForTimeout(200);

        // Width should expand on hover (CSS :hover)
        const hoverWidth = await sidebar.evaluate(el => el.offsetWidth);
        expect(hoverWidth).toBe(260); // Expands to full width on hover

        // Move mouse away
        await page.mouse.move(500, 300);
        await page.waitForTimeout(200);

        // Should collapse back
        const afterHoverWidth = await sidebar.evaluate(el => el.offsetWidth);
        expect(afterHoverWidth).toBe(68);
    });

    test('main content margin adjusts when sidebar collapses', async ({ page }) => {
        const mainContent = page.locator('.main-content');
        const toggleButton = page.locator('#sidebar-toggle');

        // Get initial margin
        const initialMargin = await mainContent.evaluate(el => {
            return parseInt(getComputedStyle(el).marginLeft);
        });
        expect(initialMargin).toBe(260);

        // Collapse sidebar
        await toggleButton.click();
        await page.waitForTimeout(200);

        // Margin should be reduced
        const collapsedMargin = await mainContent.evaluate(el => {
            return parseInt(getComputedStyle(el).marginLeft);
        });
        expect(collapsedMargin).toBe(68);
    });

    test('collapsed state is restored on page reload', async ({ page }) => {
        const sidebar = page.locator('#sidebar');
        const toggleButton = page.locator('#sidebar-toggle');

        // Collapse sidebar
        await toggleButton.click();
        await page.waitForTimeout(200);

        // Reload page
        await page.reload();
        await page.waitForSelector('#sidebar');

        // Move mouse away from sidebar to avoid hover expansion
        await page.mouse.move(500, 300);
        await page.waitForTimeout(200);

        // Sidebar should still be collapsed
        await expect(sidebar).toHaveClass(/collapsed/);

        const width = await sidebar.evaluate(el => el.offsetWidth);
        expect(width).toBe(68);
    });
});
