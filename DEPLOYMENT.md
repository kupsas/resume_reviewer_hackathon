---
description: Deploying on local
globs: 
alwaysApply: false
---

# Your rule content

- You can @ files here
- You can use markdown but dont have to

# Local Deployment Guide

## Pre-deployment Checklist
1. Ensure you're in the project root directory
2. Ensure virtual environment is available in `backend/venv`
3. Ensure all node modules are installed in `frontend`

## Port Management
### Checking for Used Ports
```bash
# Check which processes are using the development ports
lsof -i :3000-3005,8000-8005 | grep LISTEN
```

### Clearing Ports
```bash
# If ports are in use, get the PIDs and kill them
# Replace PIDs with the numbers from the lsof command
kill -9 <PID1> <PID2> <PID3>

# Alternative: Kill all processes on these ports (use with caution)
for port in {3000..3005} {8000..8005}; do
    lsof -ti :$port | xargs kill -9 2>/dev/null
done
```

## Starting Backend
1. Navigate to backend directory:
```bash
cd backend
```

2. Activate virtual environment:
```bash
source venv/bin/activate  # Unix/MacOS
# or
.\venv\Scripts\activate  # Windows
```

3. Start the FastAPI server:
```bash
# Normal start
uvicorn app.main:app --reload

# Debug mode (recommended for development)
PYTHONPATH=. python3 -m uvicorn app.main:app --reload --log-level debug
```

### Common Backend Issues
1. **Port 8000 in use**
   - Follow port clearing steps above
   - Try alternative ports (8001-8005)
   - Update frontend API calls if using different port

2. **Virtual Environment Issues**
   ```bash
   # Recreate virtual environment if needed
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **OpenAI API Issues**
   - Check `.env` file exists in backend directory
   - Verify OPENAI_API_KEY is set correctly
   - Ensure API key has sufficient credits

## Starting Frontend
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Start the Next.js development server:
```bash
npm run dev
```

### Common Frontend Issues
1. **Port 3000 in use**
   - Follow port clearing steps above
   - Next.js will automatically try ports 3001-3005
   - Note the port number in the console output

2. **Node Modules Issues**
   ```bash
   # Reinstall node modules if needed
   rm -rf node_modules
   rm package-lock.json
   npm install
   ```

3. **Build Issues**
   ```bash
   # Clear Next.js cache
   rm -rf .next
   npm run dev
   ```

## Verification Steps
1. Backend Health Check:
   - Open http://localhost:8000/docs
   - Verify Swagger UI loads
   - Check OpenAI API connection

2. Frontend Health Check:
   - Open http://localhost:3000
   - Verify page loads
   - Check browser console for errors
   - Test file upload functionality

## Debugging Tips
1. **Backend Logs**
   - Watch for 500 errors in backend console
   - Check PDF/DOCX text extraction logs
   - Monitor OpenAI API responses

2. **Frontend Logs**
   - Use browser developer tools (F12)
   - Check Network tab for API calls
   - Monitor console for component rendering logs

3. **Cross-Origin Issues**
   - Verify backend CORS settings
   - Check frontend API URL configuration
   - Ensure ports match in API calls

## Quick Reset Script
```bash
#!/bin/bash
# Save as reset-local.sh in project root

# Kill existing processes
for port in {3000..3005} {8000..8005}; do
    lsof -ti :$port | xargs kill -9 2>/dev/null
done

# Start backend
cd backend
source venv/bin/activate
PYTHONPATH=. python3 -m uvicorn app.main:app --reload --log-level debug &

# Start frontend
cd ../frontend
npm run dev &

echo "Servers starting... Check http://localhost:3000 and http://localhost:8000/docs"
```
