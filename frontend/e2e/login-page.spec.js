import { test, expect } from '@playwright/test'

test('login page contains form', async ({ page }) => {
  await page.goto('/login')
  await expect(page.getByRole('heading')).toHaveText('Login')
  await expect(page.getByRole('textbox', { name: 'username' })).toBeEditable()
  await expect(page.getByRole('textbox', { name: 'password' })).toBeEditable()
  await expect(page.getByRole('button')).toHaveText('Login')
})
