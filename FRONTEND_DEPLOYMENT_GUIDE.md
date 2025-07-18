# Frontend Deployment Guide

## Step 1: Create New Railway Service for Frontend

1. Go to your Railway dashboard
2. Click **"+ New"** → **"GitHub Repo"**
3. Select your repository
4. Choose **"Deploy from the same repo"** (different service)

## Step 2: Configure Frontend Service

**Service Settings:**
- **Name**: `team-wellness-frontend`
- **Root Directory**: `/` (keep as root)
- **Build Command**: `npm run build`
- **Start Command**: `npm run start`

**Environment Variables:**
- `PORT`: `3000`
- `VITE_API_URL`: `https://teamwellnesscompanysite-production.up.railway.app`

## Step 3: Domain Configuration

**After frontend deploys:**
1. Go to **Settings** → **Domains**
2. Click **"+ Custom Domain"**
3. Enter: `www.teamwellnesscompany.com`
4. Railway will provide DNS records to update

## Step 4: DNS Migration from Squarespace

**DNS Records to Update:**
- **Type**: CNAME
- **Name**: www
- **Value**: `[railway-frontend-url]`

**Or use A Record:**
- **Type**: A
- **Name**: www  
- **Value**: `[railway-ip-address]`

## Step 5: SSL Certificate
Railway automatically provisions SSL certificates for custom domains.