import { test, expect } from '@playwright/test';
import { Buffer } from 'buffer';

test.describe('Home Page Tests', () => {
  test('should load the home page correctly', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Verify the page has loaded by checking for a textarea (for job description)
    const textarea = page.locator('textarea');
    await expect(textarea).toBeVisible();
    
    // Check for a file input - exists but hidden is expected
    const fileInput = page.locator('input[type="file"]');
    await expect(fileInput).toBeAttached(); // Check it exists in DOM
    
    // Verify the visible upload interface instead
    const uploadArea = page.getByText(/Drag and drop your resume file/i);
    await expect(uploadArea).toBeVisible();
  });
  
  test('should have a disabled submit button initially', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Get all buttons and check if any contains "Analyze" or "Submit"
    const buttons = page.locator('button');
    const buttonCount = await buttons.count();
    
    let analyzeButton = null;
    for (let i = 0; i < buttonCount; i++) {
      const text = await buttons.nth(i).textContent();
      if (text && (text.includes('Analyze') || text.includes('Submit'))) {
        analyzeButton = buttons.nth(i);
        break;
      }
    }
    
    // Check that we found such a button and it's disabled
    expect(analyzeButton).not.toBeNull();
    if (analyzeButton) {
      await expect(analyzeButton).toBeDisabled();
    }
  });
  
  test('should enable submit button when file is selected', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Find the file input
    const fileInput = page.locator('input[type="file"]');
    
    // Upload a test file
    await fileInput.setInputFiles({
      name: 'test-resume.pdf',
      mimeType: 'application/pdf',
      buffer: Buffer.from('Fake PDF content for testing')
    });
    
    // Find analyze button that should now be enabled
    const buttons = page.locator('button');
    const buttonCount = await buttons.count();
    
    let analyzeButton = null;
    for (let i = 0; i < buttonCount; i++) {
      const text = await buttons.nth(i).textContent();
      if (text && (text.includes('Analyze') || text.includes('Submit'))) {
        analyzeButton = buttons.nth(i);
        break;
      }
    }
    
    // Check that we found such a button and it's now enabled
    expect(analyzeButton).not.toBeNull();
    if (analyzeButton) {
      await expect(analyzeButton).toBeEnabled();
    }
  });
}); 