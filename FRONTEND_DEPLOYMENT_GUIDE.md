# Frontend Deployment to Railway - Step by Step Guide

## 🚀 Railway Frontend Deployment Instructions

### Prerequisites
✅ Backend already deployed successfully to Railway
✅ Frontend tested locally and integrated with Railway backend
✅ All files prepared for deployment

### Step 1: Create New Railway Service for Frontend
1. Go to Railway Dashboard (railway.app)
2. Open your existing project (Team Wellness Company)
3. Click "Add Service" → "GitHub Repo" (or "Empty Service" if deploying via CLI)
4. If using GitHub: Select your repository and choose to deploy frontend

### Step 2: Configure Frontend Service
**Important Files Already Prepared:**
- ✅ `package.json` - Contains build and start scripts
- ✅ `yarn.lock` - Dependencies locked
- ✅ `railway-frontend.json` - Railway configuration
- ✅ `vite.config.js` - Build configuration
- ✅ `.env` - Backend URL configured

**Manual Configuration Needed in Railway Dashboard:**

#### Build & Deploy Settings:
- **Build Command**: `yarn build`
- **Start Command**: `yarn preview --port $PORT --host 0.0.0.0`
- **Root Directory**: `/` (current directory)

#### Environment Variables:
Add the following to Railway frontend service:
```
VITE_API_URL=https://teamwellnesscompanysite-production.up.railway.app
```

#### Custom Railway Configuration:
If Railway doesn't auto-detect, upload/use the `railway-frontend.json` file:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "yarn preview --port $PORT --host 0.0.0.0",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

### Step 3: Deploy Frontend
1. Trigger deployment from Railway dashboard
2. Monitor build logs for any issues
3. Wait for "Deployed" status

### Step 4: Test Deployed Frontend
Once deployed:
1. Access the generated Railway frontend URL
2. Test OAuth buttons (should redirect to backend → OAuth providers)
3. Test modals and functionality
4. Verify mobile responsiveness

### Expected Results:
- ✅ Frontend loads on Railway URL
- ✅ OAuth buttons redirect to backend then to Google/Apple/Twitter
- ✅ Modals work properly
- ✅ Responsive design across devices
- ✅ No console errors

### Step 5: Update Domain Configuration (Optional)
- Configure custom domain in Railway
- Update DNS records for www.teamwellnesscompany.com
- Test with custom domain

## 🔧 Troubleshooting

**Common Issues:**
1. **Build fails**: Check `yarn.lock` and `package.json` are present
2. **404 errors**: Ensure start command uses correct port variable `$PORT`
3. **CORS errors**: Verify backend CORS allows frontend domain
4. **Asset loading**: Check Vite build configuration

**Files Ready for Deployment:**
- ✅ Frontend source code
- ✅ Build configuration (vite.config.js)
- ✅ Dependencies (package.json, yarn.lock)
- ✅ Environment variables (.env with backend URL)
- ✅ Railway configuration (railway-frontend.json)

## ⚡ Quick Start
1. Create new Railway service
2. Upload/connect this frontend directory
3. Set start command: `yarn preview --port $PORT --host 0.0.0.0`
4. Add environment variable: `VITE_API_URL=https://teamwellnesscompanysite-production.up.railway.app`
5. Deploy!

The frontend is **READY FOR DEPLOYMENT** with all configurations prepared!