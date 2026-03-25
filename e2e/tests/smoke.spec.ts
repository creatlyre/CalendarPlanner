import { test, expect } from '@playwright/test';

test('authenticated user sees dashboard', async ({ page }) => {
  await page.goto('/');

  // Dashboard should load (not redirect to login)
  await expect(page).not.toHaveURL(/\/auth\/login/);

  // Page should have some content (not blank)
  await expect(page.locator('body')).not.toBeEmpty();
});
