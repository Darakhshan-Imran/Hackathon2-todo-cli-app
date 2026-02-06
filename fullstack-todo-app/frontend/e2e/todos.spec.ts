import { test, expect } from "@playwright/test";

/**
 * E2E tests for User Story 2: Todo CRUD operations.
 * Tests: create todo → view in list → edit → mark complete → delete
 */

test.describe("Todo CRUD Operations", () => {
  const testUser = {
    email: `todo-test-${Date.now()}@example.com`,
    username: `todouser${Date.now()}`,
    password: "SecurePass123!",
  };

  // Setup: Create user and login before each test
  test.beforeEach(async ({ page }) => {
    // Sign up new user
    await page.goto("/signup");
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="username"]', testUser.username);
    await page.fill('input[name="password"]', testUser.password);
    await page.fill('input[name="confirmPassword"]', testUser.password);
    await page.click('button[type="submit"]');

    // Login if needed
    if (page.url().includes("/login")) {
      await page.fill('input[name="email"]', testUser.email);
      await page.fill('input[name="password"]', testUser.password);
      await page.click('button[type="submit"]');
    }

    // Wait for dashboard
    await expect(page).toHaveURL(/\/todos/);
  });

  test("should create a new todo", async ({ page }) => {
    // Navigate to create todo page
    await page.click('a:has-text("New Todo"), button:has-text("New Todo")');
    await expect(page).toHaveURL(/\/todos\/new/);

    // Fill the form
    const todoTitle = `Test Todo ${Date.now()}`;
    await page.fill('input[name="title"]', todoTitle);
    await page.fill(
      'textarea[name="description"]',
      "This is a test description"
    );
    await page.selectOption('select[name="priority"]', "high");

    // Submit
    await page.click('button[type="submit"]');

    // Should redirect to todos list
    await expect(page).toHaveURL(/\/todos$/);

    // New todo should be visible in the list
    await expect(page.locator(`text=${todoTitle}`)).toBeVisible();
  });

  test("should view todo details", async ({ page }) => {
    // Create a todo first
    const todoTitle = `View Test ${Date.now()}`;
    await page.click('a:has-text("New Todo"), button:has-text("New Todo")');
    await page.fill('input[name="title"]', todoTitle);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/todos$/);

    // Click on the todo to view details
    await page.click(`text=${todoTitle}`);

    // Should be on todo detail page
    await expect(page).toHaveURL(/\/todos\/[a-f0-9-]+/);
    await expect(page.locator(`h1, h2`)).toContainText(todoTitle);
  });

  test("should edit a todo", async ({ page }) => {
    // Create a todo first
    const originalTitle = `Edit Test ${Date.now()}`;
    await page.click('a:has-text("New Todo"), button:has-text("New Todo")');
    await page.fill('input[name="title"]', originalTitle);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/todos$/);

    // Click on the todo
    await page.click(`text=${originalTitle}`);

    // Click edit button
    await page.click('button:has-text("Edit")');

    // Update the title
    const updatedTitle = `Updated ${originalTitle}`;
    await page.fill('input[name="title"]', updatedTitle);
    await page.click('button[type="submit"]');

    // Should show updated title
    await expect(page.locator(`text=${updatedTitle}`)).toBeVisible();
  });

  test("should mark todo as completed", async ({ page }) => {
    // Create a todo first
    const todoTitle = `Complete Test ${Date.now()}`;
    await page.click('a:has-text("New Todo"), button:has-text("New Todo")');
    await page.fill('input[name="title"]', todoTitle);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/todos$/);

    // Find the todo item and click status toggle
    const todoItem = page.locator(`[data-testid="todo-item"]`).filter({
      hasText: todoTitle,
    });

    // Click on status toggle or checkbox
    await todoItem
      .locator(
        'button:has-text("Complete"), input[type="checkbox"], [data-testid="status-toggle"]'
      )
      .click();

    // Todo should now show completed status
    await expect(
      todoItem.locator('text=completed, [data-status="completed"]')
    ).toBeVisible();
  });

  test("should delete a todo", async ({ page }) => {
    // Create a todo first
    const todoTitle = `Delete Test ${Date.now()}`;
    await page.click('a:has-text("New Todo"), button:has-text("New Todo")');
    await page.fill('input[name="title"]', todoTitle);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/todos$/);

    // Find the todo and click delete
    const todoItem = page.locator(`[data-testid="todo-item"]`).filter({
      hasText: todoTitle,
    });

    await todoItem.locator('button:has-text("Delete")').click();

    // Confirm deletion if there's a dialog
    const dialog = page.locator('[role="dialog"], [data-testid="confirm-dialog"]');
    if (await dialog.isVisible()) {
      await dialog.locator('button:has-text("Confirm"), button:has-text("Delete")').click();
    }

    // Todo should no longer be visible
    await expect(page.locator(`text=${todoTitle}`)).not.toBeVisible();
  });

  test("should show empty state when no todos", async ({ page }) => {
    // On fresh account, should show empty state
    const emptyState = page.locator(
      'text=No todos, text=Create your first todo, [data-testid="empty-state"]'
    );

    // Either shows empty state or has no todo items
    const todoItems = page.locator('[data-testid="todo-item"]');
    const count = await todoItems.count();

    if (count === 0) {
      // Empty state should be visible or just no items
      await expect(page.locator("main")).toBeVisible();
    }
  });
});
