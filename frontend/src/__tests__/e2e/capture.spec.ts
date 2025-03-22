import { test } from '@playwright/test';

test('capture page state', async ({ page }) => {
  // Navigate to the home page
  await page.goto('/');
  
  // Wait a bit to make sure everything is loaded
  await page.waitForTimeout(2000);
  
  // Capture the page HTML for debugging
  const html = await page.content();
  console.log('Page HTML:', html);
  
  // Also capture all button texts
  const buttonTexts = await page.getByRole('button').allTextContents();
  console.log('Button texts:', buttonTexts);
  
  // Log all labels and placeholders
  const inputLabels = await page.locator('label').allTextContents();
  console.log('Input labels:', inputLabels);
  
  const inputPlaceholders = await page.locator('input[placeholder], textarea[placeholder]').evaluateAll(
    (elements) => elements.map((el) => el.getAttribute('placeholder'))
  );
  console.log('Input placeholders:', inputPlaceholders);
  
  // This test will always pass - we just want to capture info
}); 