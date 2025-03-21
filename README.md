# Resume Reviewer UI Components Branch

> ⚠️ **IMPORTANT NOTE**: This branch (`feature/ui-components`) is dedicated to **frontend component development only**. There is no backend implementation in this branch.

## Mock Backend Implementation

Instead of relying on a real backend API, this branch uses a mock service implementation located in `frontend/src/mocks/`. The mock services simulate backend API calls with realistic data and response structures.

### How to use the mock services:

```typescript
// Import the resume service
import { resumeService } from '@/mocks';

// Use it like a real API
async function analyzeResume(file, jobDescription) {
  try {
    const result = await resumeService.analyzeResumeFile(file, jobDescription);
    // Process result...
  } catch (error) {
    // Handle errors...
  }
}
```

### Toggle between mock and real backend:

When you're ready to integrate with a real backend, set `USE_MOCKS = false` in `frontend/src/mocks/index.ts`.

## Running the Frontend

This project uses [Vite](https://vitejs.dev/) for frontend development.

### First-time setup:

```bash
# Install dependencies
cd frontend
npm install
# or if you prefer Bun
bun install
```

### Running the development server:

```bash
cd frontend
# Use NPX to run Vite directly (this works more reliably)
npx vite --port 3000
```

The application will be available at http://localhost:3000/

---

# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/353d97f4-580c-4b82-a78f-994c65e2181e