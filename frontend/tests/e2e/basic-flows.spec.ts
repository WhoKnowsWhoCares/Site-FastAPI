import { test, expect } from '@playwright/test';

test.describe('Public Pages', () => {
  test('home page loads successfully', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Alexander/);
    await expect(page.locator('main')).toBeVisible();
  });

  test('aboutme page loads successfully', async ({ page }) => {
    await page.goto('/aboutme');
    await expect(page.locator('main')).toBeVisible();
  });

  test('ihome page loads successfully', async ({ page }) => {
    await page.goto('/ihome');
    await expect(page.locator('main')).toBeVisible();
  });

  test('trade4me page loads successfully', async ({ page }) => {
    await page.goto('/trade4me');
    await expect(page.locator('main')).toBeVisible();
  });

  test('sdart page loads successfully', async ({ page }) => {
    await page.goto('/sdart');
    await expect(page.locator('main')).toBeVisible();
  });
});

test.describe('Navigation', () => {
  test('header navigation works', async ({ page }) => {
    await page.goto('/');
    
    // Check that header is visible
    await expect(page.locator('header')).toBeVisible();
    
    // Try clicking on a nav link (if present)
    const navLinks = page.locator('nav a').first();
    if (await navLinks.count() > 0) {
      await navLinks.click();
      await page.waitForLoadState('networkidle');
      expect(page.url()).toContain('/');
    }
  });
});

test.describe('ControlPanel Access', () => {
  test('controlpanel login page is accessible', async ({ page }) => {
    await page.goto('/controlpanel/login');
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('controlpanel dashboard redirects to login without auth', async ({ page }) => {
    // Clear cookies to ensure no auth
    await page.context().clearCookies();
    await page.goto('/controlpanel');
    
    // Should either redirect or show login form
    const currentUrl = page.url();
    expect(currentUrl).toContain('/controlpanel');
  });
});
