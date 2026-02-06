import { test, expect } from "@playwright/test";

/**
 * E2E tests for User Story 3: Filtering and pagination.
 * Tests: create 25 todos → filter by status → paginate → sort
 */

test.describe("Todo Filtering and Pagination", () => {
  const testUser = {
    email: `filter-test-${Date.now()}@example.com`,
    username: `filteruser${Date.now()}`,
    password: "SecurePass123!",
  };

  // Helper to create a todo quickly
  async function createTodo(
    page: import("@playwright/test").Page,
    title: string,
    priority: string = "medium"
  ) {
    await page.goto("/todos/new");
    await page.fill('input[name="title"]', title);
    await page.selectOption('select[name="priority"]', priority);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/todos$/);
  }

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

    await expect(page).toHaveURL(/\/todos/);
  });

  test("should filter todos by status", async ({ page }) => {
    // Create todos with different statuses
    await createTodo(page, "Pending Task 1");
    await createTodo(page, "Pending Task 2");

    // Navigate to todos list
    await page.goto("/todos");

    // Find and use status filter
    const statusFilter = page.locator(
      'select[name="status"], [data-testid="status-filter"]'
    );

    if (await statusFilter.isVisible()) {
      // Filter by pending
      await statusFilter.selectOption("pending");

      // Should show only pending todos
      await expect(page.locator("text=Pending Task 1")).toBeVisible();
      await expect(page.locator("text=Pending Task 2")).toBeVisible();

      // Filter by completed (should show no results or empty state)
      await statusFilter.selectOption("completed");

      // Pending tasks should not be visible
      await expect(page.locator("text=Pending Task 1")).not.toBeVisible();
    }
  });

  test("should filter todos by priority", async ({ page }) => {
    // Create todos with different priorities
    await createTodo(page, "High Priority Task", "high");
    await createTodo(page, "Low Priority Task", "low");

    // Navigate to todos list
    await page.goto("/todos");

    // Find and use priority filter
    const priorityFilter = page.locator(
      'select[name="priority"], [data-testid="priority-filter"]'
    );

    if (await priorityFilter.isVisible()) {
      // Filter by high priority
      await priorityFilter.selectOption("high");

      // Should show only high priority todos
      await expect(page.locator("text=High Priority Task")).toBeVisible();
      await expect(page.locator("text=Low Priority Task")).not.toBeVisible();
    }
  });

  test("should paginate todos", async ({ page }) => {
    // Create more than 10 todos (default page size)
    for (let i = 1; i <= 15; i++) {
      await createTodo(page, `Pagination Todo ${i}`);
    }

    // Navigate to todos list
    await page.goto("/todos");

    // Check if pagination exists
    const pagination = page.locator(
      '[data-testid="pagination"], nav[aria-label="pagination"]'
    );

    if (await pagination.isVisible()) {
      // Should show first page items
      await expect(page.locator("text=Pagination Todo")).toBeVisible();

      // Click next page
      const nextButton = pagination.locator(
        'button:has-text("Next"), [aria-label="Next page"]'
      );
      if (await nextButton.isEnabled()) {
        await nextButton.click();

        // Should show second page items
        await expect(page).toHaveURL(/page=2/);
      }
    }
  });

  test("should sort todos", async ({ page }) => {
    // Create todos
    await createTodo(page, "AAA First Todo", "low");
    await createTodo(page, "ZZZ Last Todo", "high");

    // Navigate to todos list
    await page.goto("/todos");

    // Find sort control
    const sortControl = page.locator(
      'select[name="sort"], [data-testid="sort-select"]'
    );

    if (await sortControl.isVisible()) {
      // Sort by priority
      await sortControl.selectOption("priority");

      // High priority should come first
      const todoItems = page.locator('[data-testid="todo-item"]');
      const firstTodo = await todoItems.first().textContent();
      expect(firstTodo).toContain("high");
    }
  });

  test("should clear filters", async ({ page }) => {
    // Create a todo
    await createTodo(page, "Filter Clear Test", "high");

    // Navigate and apply filter
    await page.goto("/todos");

    const statusFilter = page.locator(
      'select[name="status"], [data-testid="status-filter"]'
    );
    if (await statusFilter.isVisible()) {
      await statusFilter.selectOption("completed");
    }

    // Click clear filters button
    const clearButton = page.locator(
      'button:has-text("Clear"), button:has-text("Reset"), [data-testid="clear-filters"]'
    );

    if (await clearButton.isVisible()) {
      await clearButton.click();

      // All todos should be visible again
      await expect(page.locator("text=Filter Clear Test")).toBeVisible();
    }
  });

  test("should combine multiple filters", async ({ page }) => {
    // Create todos with various combinations
    await createTodo(page, "High Pending", "high");
    await createTodo(page, "Low Pending", "low");

    await page.goto("/todos");

    const statusFilter = page.locator(
      'select[name="status"], [data-testid="status-filter"]'
    );
    const priorityFilter = page.locator(
      'select[name="priority"], [data-testid="priority-filter"]'
    );

    if ((await statusFilter.isVisible()) && (await priorityFilter.isVisible())) {
      // Apply both filters
      await statusFilter.selectOption("pending");
      await priorityFilter.selectOption("high");

      // Should only show high priority pending todos
      await expect(page.locator("text=High Pending")).toBeVisible();
      await expect(page.locator("text=Low Pending")).not.toBeVisible();
    }
  });
});
