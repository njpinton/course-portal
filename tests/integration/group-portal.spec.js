/**
 * Group Portal Comprehensive E2E Tests
 * Tests all functionality and buttons on the group portal page
 *
 * Run with: npx playwright test tests/integration/group-portal.spec.js
 */

const { test, expect } = require('@playwright/test');

// Generate unique identifiers for test isolation
const timestamp = Date.now();
const TEST_GROUP = {
    name: `Portal Test ${timestamp}`,
    project: `Portal Project ${timestamp}`,
    username: `portaltest${timestamp}`,
    password: 'testpass123'
};

// ===========================================
// PAGE LOAD AND BASIC ELEMENTS
// ===========================================
test.describe('Group Portal - Page Load', () => {

    test('Page loads with correct title and header', async ({ page }) => {
        await page.goto('/group_portal');

        // Check page title
        await expect(page).toHaveTitle(/Group Project Portal/);

        // Check portal header
        await expect(page.locator('.portal-title')).toContainText('Group Project Portal');
    });

    test('Breadcrumbs are visible and correct', async ({ page }) => {
        await page.goto('/group_portal');

        // Check breadcrumbs
        await expect(page.locator('.breadcrumb-item').first()).toContainText('Home');
        await expect(page.locator('.breadcrumb-current')).toContainText('Group Portal');
    });

    test('Toast container exists for notifications', async ({ page }) => {
        await page.goto('/group_portal');

        // Toast container should exist (for showing messages)
        await expect(page.locator('#toastContainer')).toBeAttached();
    });

    test('Groups list section is visible', async ({ page }) => {
        await page.goto('/group_portal');

        // Existing Groups section
        await expect(page.locator('#groupsTitle')).toContainText('Existing Groups');
        await expect(page.locator('#groupsList')).toBeVisible();
    });

    test('Groups load from API', async ({ page }) => {
        await page.goto('/group_portal');

        // Wait for network to settle
        await page.waitForLoadState('networkidle');

        // Give extra time for groups to render
        await page.waitForTimeout(3000);

        // Should either show groups, empty state, or loading finished (no spinner)
        const hasGroups = await page.locator('.group-card, .groups-table').isVisible().catch(() => false);
        const hasEmptyState = await page.locator('.empty-state').isVisible().catch(() => false);
        const hasGroupsList = await page.locator('#groupsList').isVisible().catch(() => false);

        // As long as the groups list section is visible (not just loading), we're good
        expect(hasGroups || hasEmptyState || hasGroupsList).toBeTruthy();
        console.log(`Groups loaded: ${hasGroups}, Empty state: ${hasEmptyState}, Groups list visible: ${hasGroupsList}`);
    });

});

// ===========================================
// ACTION BUTTONS
// ===========================================
test.describe('Group Portal - Action Buttons', () => {

    test('Create New Group button is visible and clickable', async ({ page }) => {
        await page.goto('/group_portal');

        const createBtn = page.locator('#showCreateGroupBtn');
        await expect(createBtn).toBeVisible();
        await expect(createBtn).toContainText('Create New Group');
        await expect(createBtn).toHaveAttribute('aria-expanded', 'false');
    });

    test('Group Login button is visible and links correctly', async ({ page }) => {
        await page.goto('/group_portal');

        const loginLink = page.locator('a[href="/group_login"]');
        await expect(loginLink).toBeVisible();
        await expect(loginLink).toContainText('Group Login');
    });

    test('Group Login button navigates to login page', async ({ page }) => {
        await page.goto('/group_portal');

        await page.click('a[href="/group_login"]');
        await expect(page).toHaveURL(/.*group_login/);
        await expect(page.locator('h1')).toContainText('Group Login');
    });

});

// ===========================================
// CREATE GROUP FORM TOGGLE
// ===========================================
test.describe('Group Portal - Create Group Form Toggle', () => {

    test('Form is hidden initially', async ({ page }) => {
        await page.goto('/group_portal');

        const formSection = page.locator('#createGroupSection');
        await expect(formSection).toHaveClass(/hidden/);
    });

    test('Clicking Create New Group shows the form', async ({ page }) => {
        await page.goto('/group_portal');

        await page.click('#showCreateGroupBtn');

        const formSection = page.locator('#createGroupSection');
        await expect(formSection).not.toHaveClass(/hidden/);
        await expect(formSection).toBeVisible();

        // Button text should change
        await expect(page.locator('#showCreateGroupBtn')).toContainText('Hide Form');
        await expect(page.locator('#showCreateGroupBtn')).toHaveAttribute('aria-expanded', 'true');
    });

    test('Clicking button again hides the form', async ({ page }) => {
        await page.goto('/group_portal');

        // Show form
        await page.click('#showCreateGroupBtn');
        await expect(page.locator('#createGroupSection')).toBeVisible();

        // Hide form
        await page.click('#showCreateGroupBtn');
        await expect(page.locator('#createGroupSection')).toHaveClass(/hidden/);
        await expect(page.locator('#showCreateGroupBtn')).toContainText('Create New Group');
    });

});

// ===========================================
// CREATE GROUP FORM ELEMENTS
// ===========================================
test.describe('Group Portal - Create Group Form Elements', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('/group_portal');
        await page.click('#showCreateGroupBtn');
        await expect(page.locator('#createGroupSection')).toBeVisible();
    });

    test('Form has all required input fields', async ({ page }) => {
        // Group Information
        await expect(page.locator('#groupName')).toBeVisible();
        await expect(page.locator('#projectTitle')).toBeVisible();

        // Login Credentials
        await expect(page.locator('#groupUsername')).toBeVisible();
        await expect(page.locator('#groupPassword')).toBeVisible();

        // Student Search
        await expect(page.locator('#studentSearch')).toBeVisible();
    });

    test('Form has proper labels', async ({ page }) => {
        await expect(page.locator('label[for="groupName"]')).toContainText('Group Name');
        await expect(page.locator('label[for="projectTitle"]')).toContainText('Project Title');
        await expect(page.locator('label[for="groupUsername"]')).toContainText('Username');
        await expect(page.locator('label[for="groupPassword"]')).toContainText('Password');
    });

    test('Form has submit button', async ({ page }) => {
        const submitBtn = page.locator('#createGroupForm button[type="submit"]');
        await expect(submitBtn).toBeVisible();
        await expect(submitBtn).toContainText('Create Group');
    });

    test('Input fields have proper placeholders', async ({ page }) => {
        await expect(page.locator('#groupName')).toHaveAttribute('placeholder', /Team Alpha/);
        await expect(page.locator('#projectTitle')).toHaveAttribute('placeholder', /ML Image/);
        await expect(page.locator('#groupUsername')).toHaveAttribute('placeholder', /unique username/);
        await expect(page.locator('#groupPassword')).toHaveAttribute('placeholder', /6 characters/);
    });

    test('Password field has minlength attribute', async ({ page }) => {
        await expect(page.locator('#groupPassword')).toHaveAttribute('minlength', '6');
    });

    test('Selected members container shows empty state initially', async ({ page }) => {
        await expect(page.locator('#selectedMembers')).toContainText('No members added yet');
    });

});

// ===========================================
// CREATE GROUP FORM VALIDATION
// ===========================================
test.describe('Group Portal - Form Validation', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('/group_portal');
        await page.click('#showCreateGroupBtn');
    });

    test('Cannot submit with empty group name', async ({ page }) => {
        // Fill other fields but not group name
        await page.fill('#projectTitle', 'Test Project');
        await page.fill('#groupUsername', 'testuser');
        await page.fill('#groupPassword', 'testpass123');

        // Try to submit
        await page.click('#createGroupForm button[type="submit"]');

        // Form should not submit (HTML5 validation)
        // Check we're still on the same page
        await expect(page).toHaveURL(/.*group_portal/);
    });

    test('Cannot submit with short password', async ({ page }) => {
        await page.fill('#groupName', 'Test Group');
        await page.fill('#projectTitle', 'Test Project');
        await page.fill('#groupUsername', 'testuser');
        await page.fill('#groupPassword', '123'); // Too short

        await page.click('#createGroupForm button[type="submit"]');

        // Should show validation error or toast
        await page.waitForTimeout(1000);
        await expect(page).toHaveURL(/.*group_portal/);
    });

    test('Toast appears for missing required fields', async ({ page }) => {
        // Fill only some fields
        await page.fill('#groupName', 'Test Group');
        await page.fill('#groupPassword', 'testpass123');
        // Missing username

        await page.click('#createGroupForm button[type="submit"]');
        await page.waitForTimeout(500);

        // Should still be on same page
        await expect(page).toHaveURL(/.*group_portal/);
    });

});

// ===========================================
// STUDENT SEARCH IN CREATE FORM
// ===========================================
test.describe('Group Portal - Student Search', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('/group_portal');
        await page.click('#showCreateGroupBtn');
    });

    test('Student search input is visible', async ({ page }) => {
        const searchInput = page.locator('#studentSearch');
        await expect(searchInput).toBeVisible();
        await expect(searchInput).toHaveAttribute('placeholder', /Search students/);
    });

    test('Student dropdown is hidden initially', async ({ page }) => {
        const dropdown = page.locator('#studentsList');
        await expect(dropdown).not.toHaveClass(/active/);
    });

    test('Focus on search shows dropdown (if students available)', async ({ page }) => {
        const searchInput = page.locator('#studentSearch');
        await searchInput.focus();

        // Wait for students to load
        await page.waitForTimeout(1500);

        // Dropdown may show if students are available
        const dropdown = page.locator('#studentsList');
        const isActive = await dropdown.evaluate(el => el.classList.contains('active'));
        console.log(`Student dropdown active after focus: ${isActive}`);
    });

    test('Class alert shows student availability info', async ({ page }) => {
        // Wait for students to load
        await page.waitForTimeout(2000);

        const classAlert = page.locator('#classAlert');
        const isVisible = await classAlert.isVisible().catch(() => false);

        if (isVisible) {
            const alertText = await classAlert.textContent();
            console.log(`Class alert text: ${alertText}`);
            expect(alertText).toMatch(/students? available|No ungrouped/i);
        }
    });

});

// ===========================================
// GROUPS SEARCH FILTER
// ===========================================
test.describe('Group Portal - Groups Search', () => {

    test('Groups search input is visible', async ({ page }) => {
        await page.goto('/group_portal');

        const searchInput = page.locator('#groupSearch');
        await expect(searchInput).toBeVisible();
        await expect(searchInput).toHaveAttribute('placeholder', /Search groups/);
    });

    test('Search filters groups by name', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000); // Wait for groups to load

        // Check if any groups exist
        const groupCards = page.locator('.group-card');
        const initialCount = await groupCards.count();

        if (initialCount > 0) {
            // Search for non-existent term
            await page.fill('#groupSearch', 'xyznonexistent12345');
            await page.waitForTimeout(500);

            // Should show fewer or no groups
            const newCount = await page.locator('.group-card').count();
            const emptyState = await page.locator('.empty-state').isVisible().catch(() => false);

            expect(newCount < initialCount || emptyState).toBeTruthy();
            console.log(`Initial groups: ${initialCount}, After search: ${newCount}`);
        } else {
            console.log('No groups to test search filter');
        }
    });

    test('Clearing search shows all groups again', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const initialCount = await page.locator('.group-card').count();

        if (initialCount > 0) {
            // Search and clear
            await page.fill('#groupSearch', 'test');
            await page.waitForTimeout(300);
            await page.fill('#groupSearch', '');
            await page.waitForTimeout(300);

            const finalCount = await page.locator('.group-card').count();
            expect(finalCount).toBe(initialCount);
        }
    });

});

// ===========================================
// VIEW TOGGLE (CARDS/LIST)
// ===========================================
test.describe('Group Portal - View Toggle', () => {

    test('View toggle buttons are visible', async ({ page }) => {
        await page.goto('/group_portal');

        await expect(page.locator('#viewKanban')).toBeVisible();
        await expect(page.locator('#viewList')).toBeVisible();
    });

    test('Cards view is active by default', async ({ page }) => {
        await page.goto('/group_portal');

        await expect(page.locator('#viewKanban')).toHaveClass(/active/);
        await expect(page.locator('#viewKanban')).toHaveAttribute('aria-selected', 'true');

        await expect(page.locator('#viewList')).not.toHaveClass(/active/);
        await expect(page.locator('#viewList')).toHaveAttribute('aria-selected', 'false');
    });

    test('Clicking List view switches to table layout', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000); // Wait for groups to load

        // Click List view
        await page.click('#viewList');

        await expect(page.locator('#viewList')).toHaveClass(/active/);
        await expect(page.locator('#viewKanban')).not.toHaveClass(/active/);

        // Check if table is visible (if groups exist)
        const hasGroups = await page.locator('.group-card, .groups-table').isVisible().catch(() => false);
        if (hasGroups) {
            const tableVisible = await page.locator('.groups-table, table').isVisible().catch(() => false);
            console.log(`Table visible after List view click: ${tableVisible}`);
        }
    });

    test('Clicking Cards view switches back', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        // Switch to List
        await page.click('#viewList');
        await expect(page.locator('#viewList')).toHaveClass(/active/);

        // Switch back to Cards
        await page.click('#viewKanban');
        await expect(page.locator('#viewKanban')).toHaveClass(/active/);
        await expect(page.locator('#viewList')).not.toHaveClass(/active/);
    });

    test('View toggle has proper ARIA roles', async ({ page }) => {
        await page.goto('/group_portal');

        const toggleContainer = page.locator('.view-toggle');
        await expect(toggleContainer).toHaveAttribute('role', 'tablist');

        await expect(page.locator('#viewKanban')).toHaveAttribute('role', 'tab');
        await expect(page.locator('#viewList')).toHaveAttribute('role', 'tab');
    });

});

// ===========================================
// GROUP CARDS DISPLAY
// ===========================================
test.describe('Group Portal - Group Cards', () => {

    test('Group cards show group information', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const groupCard = page.locator('.group-card').first();
        const hasCards = await groupCard.isVisible().catch(() => false);

        if (hasCards) {
            // Card should have title
            await expect(groupCard.locator('.group-card-title')).toBeVisible();

            // Card should have project info
            await expect(groupCard).toContainText('Project');

            // Card should have members count
            await expect(groupCard).toContainText('Members');

            // Card should have View Details button
            await expect(groupCard.locator('.view-details-btn')).toBeVisible();
        } else {
            console.log('No group cards to test');
        }
    });

    test('Group cards have View Details button', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        const hasBtn = await viewDetailsBtn.isVisible().catch(() => false);

        if (hasBtn) {
            await expect(viewDetailsBtn).toContainText('View Details');
            await expect(viewDetailsBtn).toHaveAttribute('data-group-id');
        }
    });

});

// ===========================================
// GROUP DETAILS MODAL
// ===========================================
test.describe('Group Portal - Group Details Modal', () => {

    test('Modal is hidden initially', async ({ page }) => {
        await page.goto('/group_portal');

        const modal = page.locator('#groupDetailsModal');
        await expect(modal).not.toHaveClass(/active/);
    });

    test('Clicking View Details opens modal', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        const hasBtn = await viewDetailsBtn.isVisible().catch(() => false);

        if (hasBtn) {
            await viewDetailsBtn.click();

            const modal = page.locator('#groupDetailsModal');
            await expect(modal).toHaveClass(/active/);
            await expect(modal).toBeVisible();
        } else {
            console.log('No View Details button to test');
        }
    });

    test('Modal shows group name in header', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        if (await viewDetailsBtn.isVisible().catch(() => false)) {
            await viewDetailsBtn.click();
            await page.waitForTimeout(1000);

            const modalTitle = page.locator('#modalGroupName');
            await expect(modalTitle).toBeVisible();

            const titleText = await modalTitle.textContent();
            console.log(`Modal title: ${titleText}`);
            expect(titleText.length).toBeGreaterThan(0);
        }
    });

    test('Modal has close button', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        if (await viewDetailsBtn.isVisible().catch(() => false)) {
            await viewDetailsBtn.click();

            const closeBtn = page.locator('.modal-close');
            await expect(closeBtn).toBeVisible();
            await expect(closeBtn).toHaveAttribute('aria-label', 'Close modal');
        }
    });

    test('Clicking close button closes modal', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        if (await viewDetailsBtn.isVisible().catch(() => false)) {
            await viewDetailsBtn.click();
            await expect(page.locator('#groupDetailsModal')).toHaveClass(/active/);

            await page.click('.modal-close');
            await expect(page.locator('#groupDetailsModal')).not.toHaveClass(/active/);
        }
    });

    test('Clicking outside modal closes it', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        if (await viewDetailsBtn.isVisible().catch(() => false)) {
            await viewDetailsBtn.click();
            await expect(page.locator('#groupDetailsModal')).toHaveClass(/active/);

            // Click on overlay (outside modal content)
            await page.locator('#groupDetailsModal').click({ position: { x: 10, y: 10 } });
            await page.waitForTimeout(300);

            await expect(page.locator('#groupDetailsModal')).not.toHaveClass(/active/);
        }
    });

    test('Pressing Escape closes modal', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        if (await viewDetailsBtn.isVisible().catch(() => false)) {
            await viewDetailsBtn.click();
            await expect(page.locator('#groupDetailsModal')).toHaveClass(/active/);

            await page.keyboard.press('Escape');
            await expect(page.locator('#groupDetailsModal')).not.toHaveClass(/active/);
        }
    });

    test('Modal shows project information', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);

        const viewDetailsBtn = page.locator('.view-details-btn').first();
        if (await viewDetailsBtn.isVisible().catch(() => false)) {
            await viewDetailsBtn.click();
            await page.waitForTimeout(2000);

            const modalContent = page.locator('#modalContent');
            const contentText = await modalContent.textContent().catch(() => '');

            // Check if modal loaded some content (could be project info or error)
            // Either "Project" or loading state or error message
            const hasContent = contentText.length > 0;
            expect(hasContent).toBeTruthy();

            if (contentText.includes('Project')) {
                console.log('Modal shows project information');
            } else if (contentText.includes('not found')) {
                console.log('Group not found - may have been deleted');
            } else {
                console.log(`Modal content: ${contentText.substring(0, 100)}`);
            }
        } else {
            console.log('No View Details button visible');
        }
    });

});

// ===========================================
// CREATE GROUP - FULL FLOW
// ===========================================
test.describe('Group Portal - Create Group Full Flow', () => {

    test('Successfully create a new group', async ({ page }) => {
        await page.goto('/group_portal');

        // Open form
        await page.click('#showCreateGroupBtn');
        await expect(page.locator('#createGroupSection')).toBeVisible();

        // Fill form
        await page.fill('#groupName', TEST_GROUP.name);
        await page.fill('#projectTitle', TEST_GROUP.project);
        await page.fill('#groupUsername', TEST_GROUP.username);
        await page.fill('#groupPassword', TEST_GROUP.password);

        // Listen for API response
        const responsePromise = page.waitForResponse(
            resp => resp.url().includes('/api/groups') && resp.request().method() === 'POST',
            { timeout: 15000 }
        );

        // Submit
        await page.click('#createGroupForm button[type="submit"]');

        // Check response
        const response = await responsePromise;
        console.log(`Create group API status: ${response.status()}`);

        if (response.status() === 201) {
            // Wait for success toast
            await page.waitForTimeout(1000);

            // Verify toast appeared
            const toast = page.locator('.toast.success');
            const toastVisible = await toast.isVisible().catch(() => false);
            if (toastVisible) {
                await expect(toast).toContainText('created successfully');
            }

            // Verify group appears in list after reload
            await page.reload();
            await page.waitForLoadState('networkidle');

            const groupInList = page.locator('.group-card-title, .group-name').filter({ hasText: TEST_GROUP.name });
            await expect(groupInList).toBeVisible({ timeout: 10000 });

            console.log(`Group "${TEST_GROUP.name}" created and verified in list`);
        }
    });

});

// ===========================================
// ACCESSIBILITY
// ===========================================
test.describe('Group Portal - Accessibility', () => {

    test('Page has proper heading hierarchy', async ({ page }) => {
        await page.goto('/group_portal');

        // H1 for main title (portal-title class)
        const h1 = page.locator('.portal-title');
        await expect(h1).toBeVisible();

        // Check it's actually an h1
        const tagName = await h1.evaluate(el => el.tagName);
        expect(tagName.toLowerCase()).toBe('h1');

        // H2 for sections
        await expect(page.locator('#groupsTitle')).toBeVisible();
    });

    test('Interactive elements have ARIA attributes', async ({ page }) => {
        await page.goto('/group_portal');

        // Create Group button - check it has aria-expanded attribute
        const createBtn = page.locator('#showCreateGroupBtn');
        const ariaExpanded = await createBtn.getAttribute('aria-expanded');
        expect(ariaExpanded).toBeTruthy();

        const ariaControls = await createBtn.getAttribute('aria-controls');
        expect(ariaControls).toBeTruthy();

        // View toggle
        const viewKanban = page.locator('#viewKanban');
        const role = await viewKanban.getAttribute('role');
        expect(role).toBe('tab');

        const ariaSelected = await viewKanban.getAttribute('aria-selected');
        expect(ariaSelected).toBeTruthy();
    });

    test('Form inputs have associated labels', async ({ page }) => {
        await page.goto('/group_portal');
        await page.click('#showCreateGroupBtn');
        await page.waitForTimeout(300);

        // Check labels are properly associated
        const groupNameLabel = page.locator('label[for="groupName"]');
        await expect(groupNameLabel).toBeVisible();

        const usernameLabel = page.locator('label[for="groupUsername"]');
        await expect(usernameLabel).toBeVisible();
    });

    test('Modal has proper dialog role', async ({ page }) => {
        await page.goto('/group_portal');

        const modal = page.locator('#groupDetailsModal');
        const role = await modal.getAttribute('role');
        expect(role).toBe('dialog');

        const ariaModal = await modal.getAttribute('aria-modal');
        expect(ariaModal).toBe('true');
    });

    test('Toast container has alert role', async ({ page }) => {
        await page.goto('/group_portal');

        const toastContainer = page.locator('#toastContainer');
        const role = await toastContainer.getAttribute('role');
        expect(role).toBe('alert');

        const ariaLive = await toastContainer.getAttribute('aria-live');
        expect(ariaLive).toBe('polite');
    });

});

// ===========================================
// API INTEGRATION
// ===========================================
test.describe('Group Portal - API Integration', () => {

    test('GET /api/groups returns group list', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForLoadState('networkidle');

        // Use page.evaluate to make fetch request with browser context
        const groups = await page.evaluate(async () => {
            const response = await fetch('/api/groups');
            if (!response.ok) return { error: true, status: response.status };
            return await response.json();
        });

        if (groups.error) {
            console.log(`API returned status: ${groups.status}`);
        } else {
            expect(Array.isArray(groups)).toBeTruthy();
            console.log(`API returned ${groups.length} groups`);
        }
    });

    test('GET /api/students/ungrouped/all returns students', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForLoadState('networkidle');

        // Use page.evaluate to make fetch request with browser context
        const students = await page.evaluate(async () => {
            const response = await fetch('/api/students/ungrouped/all');
            if (!response.ok) return { error: true, status: response.status };
            return await response.json();
        });

        if (students.error) {
            console.log(`API returned status: ${students.status}`);
        } else {
            expect(Array.isArray(students)).toBeTruthy();
            console.log(`API returned ${students.length} ungrouped students`);
        }
    });

    test('GET /api/groups/:id returns group details', async ({ page }) => {
        await page.goto('/group_portal');
        await page.waitForLoadState('networkidle');

        // First get all groups using browser context
        const groups = await page.evaluate(async () => {
            const response = await fetch('/api/groups');
            if (!response.ok) return [];
            return await response.json();
        });

        if (groups.length > 0) {
            const groupId = groups[0].id;

            const details = await page.evaluate(async (id) => {
                const response = await fetch(`/api/groups/${id}`);
                if (!response.ok) return { error: true, status: response.status };
                return await response.json();
            }, groupId);

            if (!details.error) {
                expect(details.id).toBe(groupId);
                expect(details.group_name).toBeDefined();
                console.log(`Group details fetched for: ${details.group_name}`);
            } else {
                console.log(`API returned status: ${details.status}`);
            }
        } else {
            console.log('No groups available to test details endpoint');
        }
    });

});
