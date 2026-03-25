import { test, expect } from '@playwright/test';

test.describe('Notifications', () => {
  test('bell icon visible in navbar', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    await expect(page.locator('#notification-bell-container')).toBeVisible();
    await expect(page.locator('#notification-bell')).toBeVisible();
  });

  test('bell click loads notification dropdown', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    // Bell button should be visible
    await expect(page.locator('#notification-bell')).toBeVisible();

    // Click bell — HTMX fetches /notifications/dropdown and populates panel
    await page.locator('#notification-bell').click();

    // Wait for notification panel to have content loaded by HTMX
    // The hx-on::after-request handler removes 'hidden' class
    await expect(page.locator('#notification-panel')).not.toHaveClass(/hidden/, { timeout: 10_000 });
  });
});
