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

    await expect(page.getByText(/2026-08-20|August 20, 2026/i).first()).toBeVisible();
    await expect(
      page.getByRole('button', { name: /When will it arrive\?.*4 messages/i }).first(),
    ).toBeVisible();
  });

  test('uses header search and account actions to reach support flows', async ({ page }) => {
    await page.goto('/');

    await page
      .getByPlaceholder('Search orders, returns, warranty, or products')
      .fill('Recommend a budget keyboard under $50');
    await page.keyboard.press('Enter');

    await expect(page.getByText('Mechanical Keyboard Lite', { exact: true })).toBeVisible({
      timeout: 15000,
    });

    await page.getByRole('button', { name: 'Account' }).click();
    await expect(page.getByRole('heading', { name: 'Demo customer profile' })).toBeVisible();

    await page.getByRole('button', { name: 'Ask about returns' }).click();
    await expect(page.getByText(/return headphones after 40 days/i)).toBeVisible({
      timeout: 15000,
    });
  });

  test('uses faster-help shortcuts from the side panel', async ({ page }) => {
    await page.goto('/');

    await page.getByRole('button', { name: 'Use order 1001' }).click();
    await expect(
      page.getByPlaceholder('Ask about an order, return, warranty, or product'),
    ).toHaveValue('I need help with order 1001');

    await page.getByRole('button', { name: 'Track latest order' }).click();
    await expect(page.getByText('TRK-1001', { exact: true }).first()).toBeVisible({
      timeout: 15000,
    });
  });
});
