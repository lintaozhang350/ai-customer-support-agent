import { expect, test } from '@playwright/test';

test.describe('Customer support assistant', () => {
  test('shows order details for an order lookup', async ({ page }) => {
    await page.goto('/');

    await page.getByRole('button', { name: /New conversation/i }).first().click();
    await page
      .getByPlaceholder('Ask about an order, return, warranty, or product')
      .fill('Where is my order 1001?');
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText('TRK-1001', { exact: true }).first()).toBeVisible({
      timeout: 15000,
    });
    await expect(page.getByText('Order 1001').first()).toBeVisible();
    await expect(page.getByText('Wireless Keyboard').first()).toBeVisible();
    await expect(page.getByText('Estimated delivery', { exact: true })).toBeVisible();
  });

  test('uses conversation context for a follow-up question', async ({ page }) => {
    await page.goto('/');

    await page.getByRole('button', { name: /New conversation/i }).first().click();
    await page
      .getByPlaceholder('Ask about an order, return, warranty, or product')
      .fill('Where is my order 1001?');
    await page.getByRole('button', { name: 'Send' }).click();
    await expect(page.getByText('TRK-1001', { exact: true }).first()).toBeVisible({
      timeout: 15000,
    });

    await page
      .getByPlaceholder('Ask about an order, return, warranty, or product')
      .fill('When will it arrive?');
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText(/arrive on August 20, 2026/i)).toBeVisible();
    await expect(
      page.getByRole('button', { name: /When will it arrive\?.*4 messages/i }).first(),
    ).toBeVisible();
  });
});
