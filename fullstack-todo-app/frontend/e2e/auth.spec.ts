import { test, expect } from "@playwright/test";

/**
 * E2E tests for User Story 1: Authentication flow.
 * Tests: signup → login → access dashboard → logout
 */

test.describe("Authentication Flow", () => {
  const testUser = {
    email: `test-${Date.now()}@example.com`,
    username: `testuser${Date.now()}`,
    password: "SecurePass123!",
  };

  test("should complete full authentication flow", async ({ page }) => {
    // 1. Navigate to signup page
    await page.goto("/signup");
    await expect(page).toHaveTitle(/Sign Up|Todo/i);

    // 2. Fill signup form
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="username"]', testUser.username);
    await page.fill('input[name="password"]', testUser.password);
    await page.fill('input[name="confirmPassword"]', testUser.password);

    // 3. Submit signup form
    await page.click('button[type="submit"]');

    // 4. Should redirect to login or dashboard
    await expect(page).toHaveURL(/\/(login|todos)/);

    // 5. If redirected to login, perform login
    if (page.url().includes("/login")) {
      await page.fill('input[name="email"]', testUser.email);
      await page.fill('input[name="password"]', testUser.password);
      await page.click('button[type="submit"]');
    }

    // 6. Should be on dashboard/todos page
    await expect(page).toHaveURL(/\/todos/);

    // 7. Verify user is logged in (header shows username or email)
    await expect(page.locator("header")).toContainText(
      new RegExp(testUser.username, "i")
    );

    // 8. Logout
    await page.click('button:has-text("Logout"), a:has-text("Logout")');

    // 9. Should redirect to login page
    await expect(page).toHaveURL(/\/(login|$)/);
  });

  test("should show validation errors for invalid signup", async ({ page }) => {
    await page.goto("/signup");

    // Submit empty form
    await page.click('button[type="submit"]');

    // Should show validation errors
    await expect(page.locator("text=required")).toBeVisible();
  });

  test("should show error for invalid login credentials", async ({ page }) => {
    await page.goto("/login");

    await page.fill('input[name="email"]', "nonexistent@example.com");
    await page.fill('input[name="password"]', "wrongpassword");
    await page.click('button[type="submit"]');

    // Should show error message
    await expect(page.locator('[role="alert"]')).toBeVisible();
  });

  test("should redirect to login when accessing protected route", async ({
    page,
  }) => {
    // Try to access todos without being logged in
    await page.goto("/todos");

    // Should redirect to login
    await expect(page).toHaveURL(/\/login/);
  });

  test("should persist session after page refresh", async ({ page }) => {
    // Login first
    await page.goto("/login");
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');

    // Wait for redirect to dashboard
    await expect(page).toHaveURL(/\/todos/);

    // Refresh the page
    await page.reload();

    // Should still be on dashboard (session persisted)
    await expect(page).toHaveURL(/\/todos/);
  });
});
