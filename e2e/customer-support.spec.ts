import { expect, test } from '@playwright/test';

test.describe('Customer support assistant', () => {
  test('shows order details for an order lookup', async ({ page }) => {
    await page.goto('/');

    await page.getByRole('button', { name: /New conversation/i }).first().click();
    await page.getByPlaceholder('Message customer service').fill('Where is my order 1001?');
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText('Your order 1001 for Wireless Keyboard')).toBeVisible();
    await expect(page.getByText('TRK-1001', { exact: true }).first()).toBeVisible();
    await expect(page.getByText('Estimated delivery')).toBeVisible();
  });

  test('uses conversation context for a follow-up question', async ({ page }) => {
    await page.goto('/');

    await page.getByRole('button', { name: /New conversation/i }).first().click();
    await page.getByPlaceholder('Message customer service').fill('Where is my order 1001?');
    await page.getByRole('button', { name: 'Send' }).click();
    await expect(page.getByText('TRK-1001', { exact: true }).first()).toBeVisible();

    await page.getByPlaceholder('Message customer service').fill('When will it arrive?');
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText('estimated to arrive on 2026-08-20')).toBeVisible();
    await expect(
      page.getByRole('button', { name: /When will it arrive\?.*4 messages/i }).first(),
    ).toBeVisible();
  });
});
