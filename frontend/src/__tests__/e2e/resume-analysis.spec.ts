import { test, expect } from '@playwright/test';
import { Buffer } from 'buffer';

// Mock the API response for resume analysis to avoid actual API calls
test.beforeEach(async ({ page }) => {
  // Navigate to the page and wait for it to load
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  
  // Mock the analyze resume API endpoint
  await page.route('**/api/resume/analyze/file', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'success',
        resumeAnalysis: {
          sections: [
            {
              type: 'EXPERIENCE',
              points: [
                {
                  text: 'Sample experience point',
                  star: {
                    situation: true,
                    task: true,
                    action: true,
                    result: true,
                    complete: true
                  },
                  metrics: ['metric1'],
                  technical_score: 4.5,
                  improvement: 'Sample improvement suggestion'
                }
              ]
            },
            {
              type: 'EDUCATION',
              points: [
                {
                  text: 'Sample education point',
                  star: {
                    situation: false,
                    task: false,
                    action: false,
                    result: false,
                    complete: false
                  },
                  metrics: [],
                  technical_score: 3.0,
                  improvement: 'Sample education improvement'
                }
              ]
            }
          ],
          recommendations: [
            'Add more measurable achievements',
            'Improve STAR format in bullets'
          ]
        },
        tokenUsage: {
          total_tokens: 1000,
          prompt_tokens: 500,
          completion_tokens: 500,
          total_cost: 0.02
        }
      })
    });
  });
  
  // Mock the health check endpoint
  await page.route('**/health', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'healthy' })
    });
  });
});

test.describe('Resume Analysis Flow', () => {
  test('should analyze a resume file and show results', async ({ page }) => {
    // Navigate to the home page (already done in beforeEach)
    
    // Find the file input
    const fileInput = page.locator('input[type="file"]');
    
    // Upload the test file
    await fileInput.setInputFiles({
      name: 'test-resume.pdf',
      mimeType: 'application/pdf',
      buffer: Buffer.from('Fake resume content for testing')
    });
    
    // Add a job description (optional)
    const textarea = page.locator('textarea');
    await textarea.fill('This is a test job description');
    
    // Find and click the analyze button
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
    
    expect(analyzeButton).not.toBeNull();
    if (analyzeButton) {
      await expect(analyzeButton).toBeEnabled();
      await analyzeButton.click();
    } else {
      throw new Error('Could not find analyze button');
    }
    
    // Since we're mocking, look for the expected results
    // We'll just check for some of the content we provided in the mock
    await page.waitForTimeout(1000); // Give time for results to appear
    await expect(page.getByText('Sample experience point')).toBeVisible();
  });
  
  test('should show error message when API fails', async ({ page }) => {
    // Override the mock to simulate an API error
    await page.route('**/api/resume/analyze/file', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          detail: 'Server error occurred'
        })
      });
    });
    
    // Find the file input
    const fileInput = page.locator('input[type="file"]');
    
    // Upload a test file
    await fileInput.setInputFiles({
      name: 'test-resume.pdf',
      mimeType: 'application/pdf',
      buffer: Buffer.from('Fake resume content')
    });
    
    // Find and click the analyze button
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
    
    expect(analyzeButton).not.toBeNull();
    if (analyzeButton) {
      await analyzeButton.click();
    } else {
      throw new Error('Could not find analyze button');
    }
    
    // Wait longer for error to be displayed
    await page.waitForTimeout(2000);
    
    // Create multiple locators for different possible error indicators
    const errorLocators = [
      page.getByText('Server error', { exact: false }),
      page.getByText('Error', { exact: false }),
      page.getByText('Failed', { exact: false }),
      page.locator('[role="alert"]')
    ];
    
    // Check if at least one error indicator is visible
    let errorFound = false;
    for (const locator of errorLocators) {
      const isVisible = await locator.isVisible();
      if (isVisible) {
        errorFound = true;
        break;
      }
    }
    
    // Assert that we found at least one error indicator
    expect(errorFound, 'Expected to find an error message on the page').toBeTruthy();
  });
}); 