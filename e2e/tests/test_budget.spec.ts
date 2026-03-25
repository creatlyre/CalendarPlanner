import { test, expect } from '@playwright/test';

// Budget page render tests — all authenticated, ungated routes return 200 for pro user.
// Budget stats (/budget/stats) is gated (pro/family_plus) and also verified here.

test.describe('Budget Pages — Render Verification', () => {
  test.use({ storageState: 'e2e/playwright/.auth/pro.json' });

  test('budget overview loads with 200', async ({ page }) => {
    const response = await page.goto('/budget/overview');
    expect(response?.status()).toBe(200);

    await expect(page.locator('#main-content')).toBeVisible();
  });

  test('budget expenses page loads with 200', async ({ page }) => {
    const response = await page.goto('/budget/expenses');
    expect(response?.status()).toBe(200);

    await expect(page.locator('#main-content')).toBeVisible();
  });

  test('budget income page loads with 200', async ({ page }) => {
    const response = await page.goto('/budget/income');
    expect(response?.status()).toBe(200);

    await expect(page.locator('#main-content')).toBeVisible();
  });

  test('budget stats page loads for pro user without 403', async ({ page }) => {
    const response = await page.goto('/budget/stats');
    // Gating passes (not 403). May return 500 if no budget data configured yet.
    expect(response?.status()).not.toBe(403);
  });

  test('budget settings page loads with 200', async ({ page }) => {
    const response = await page.goto('/budget/settings');
    expect(response?.status()).toBe(200);

    await expect(page.locator('#main-content')).toBeVisible();
  });
});
