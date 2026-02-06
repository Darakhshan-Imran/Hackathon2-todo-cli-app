import { test, expect } from "@playwright/test";

/**
 * E2E tests for User Story 4: Profile management.
 * Tests: view profile → update username → verify change
 */

test.describe("Profile Management", () => {
  const testUser = {
    email: `profile-test-${Date.now()}@example.com`,
    username: `profileuser${Date.now()}`,
    password: "SecurePass123!",
  };

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

  test("should view profile information", async ({ page }) => {
    // Navigate to profile page
    await page.click('a:has-text("Profile"), [data-testid="profile-link"]');
    await expect(page).toHaveURL(/\/profile/);

    // Should display user information
    await expect(page.locator(`text=${testUser.email}`)).toBeVisible();
    await expect(page.locator(`text=${testUser.username}`)).toBeVisible();
  });

  test("should update username successfully", async ({ page }) => {
    // Navigate to profile page
    await page.goto("/profile");

    // Click edit button
    await page.click('button:has-text("Edit")');

    // Enter new username
    const newUsername = `updated${Date.now()}`;
    await page.fill('input[name="username"]', newUsername);

    // Save changes
    await page.click('button[type="submit"], button:has-text("Save")');

    // Should show success message
    await expect(
      page.locator('text=success, text=updated, [role="alert"]')
    ).toBeVisible();

    // New username should be displayed
    await expect(page.locator(`text=${newUsername}`)).toBeVisible();
  });

  test("should show error for duplicate username", async ({ page, browser }) => {
    // Create another user in a different context
    const otherContext = await browser.newContext();
    const otherPage = await otherContext.newPage();

    const otherUser = {
      email: `other-${Date.now()}@example.com`,
      username: `otheruser${Date.now()}`,
      password: "SecurePass123!",
    };

    await otherPage.goto("/signup");
    await otherPage.fill('input[name="email"]', otherUser.email);
    await otherPage.fill('input[name="username"]', otherUser.username);
    await otherPage.fill('input[name="password"]', otherUser.password);
    await otherPage.fill('input[name="confirmPassword"]', otherUser.password);
    await otherPage.click('button[type="submit"]');
    await otherContext.close();

    // Now try to update to that username
    await page.goto("/profile");
    await page.click('button:has-text("Edit")');
    await page.fill('input[name="username"]', otherUser.username);
    await page.click('button[type="submit"], button:has-text("Save")');

    // Should show error
    await expect(
      page.locator('text=taken, text=conflict, text=already exists, [role="alert"]')
    ).toBeVisible();
  });

  test("should validate username format", async ({ page }) => {
    await page.goto("/profile");
    await page.click('button:has-text("Edit")');

    // Try invalid username (too short)
    await page.fill('input[name="username"]', "ab");
    await page.click('button[type="submit"], button:has-text("Save")');

    // Should show validation error
    await expect(
      page.locator('text=invalid, text=at least, text=characters')
    ).toBeVisible();
  });

  test("should cancel profile edit", async ({ page }) => {
    await page.goto("/profile");

    // Store original username
    const originalUsername = testUser.username;

    // Click edit
    await page.click('button:has-text("Edit")');

    // Type new username but don't save
    await page.fill('input[name="username"]', "tempname");

    // Click cancel
    await page.click('button:has-text("Cancel")');

    // Should still show original username
    await expect(page.locator(`text=${originalUsername}`)).toBeVisible();
  });

  test("should show email as read-only", async ({ page }) => {
    await page.goto("/profile");

    // Email field should be visible but read-only
    const emailField = page.locator(`text=${testUser.email}`);
    await expect(emailField).toBeVisible();

    // Should indicate email cannot be changed
    await expect(
      page.locator('text=cannot be changed, text=read-only')
    ).toBeVisible();
  });

  test("should show member since date", async ({ page }) => {
    await page.goto("/profile");

    // Should display member since / created date
    await expect(
      page.locator('text=Member since, text=Joined, text=Created')
    ).toBeVisible();
  });
});
