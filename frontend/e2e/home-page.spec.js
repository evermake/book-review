import { test, expect } from '@playwright/test'

test('home page contains title and search box', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading')).toHaveText('Welcome to Book Review Platform!')
  await expect(page.getByRole('searchbox')).toBeEditable()
})
