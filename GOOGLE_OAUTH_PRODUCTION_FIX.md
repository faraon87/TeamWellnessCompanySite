# Google OAuth Production Configuration Fix

## Issue Identified
During production testing, Google OAuth returned "invalid_client" error. This is because Google Cloud Console is configured for development URLs, not production.

## Required Fix

### Step 1: Update Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Credentials**
3. Find your OAuth 2.0 Client ID: `633663200476-vhkohcsihseftdgadum1psjv75ieqfbv.apps.googleusercontent.com`

### Step 2: Update Authorized Redirect URIs
**Current Configuration** (likely has):
- `http://localhost:8001/api/auth/google/callback`

**Add Production URL**:
- `https://teamwellnesscompanysite-production.up.railway.app/api/auth/google/callback`

**For Future Custom Domain** (add when ready):
- `https://www.teamwellnesscompany.com/api/auth/google/callback`

### Step 3: Update Authorized JavaScript Origins
**Add**:
- `https://twc-website-front-end-production.up.railway.app`
- `https://teamwellnesscompanysite-production.up.railway.app`

**For Future Custom Domain**:
- `https://www.teamwellnesscompany.com`

### Expected Result
After updating these settings:
- ✅ Google OAuth will work perfectly on production
- ✅ Complete OAuth integration (Google + Apple + Twitter/X)
- ✅ Ready for custom domain migration

## Current Status
- Apple OAuth: ✅ Working perfectly
- Twitter/X OAuth: ✅ Working perfectly  
- Google OAuth: ⚠️ Needs production URL configuration