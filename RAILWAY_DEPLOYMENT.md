# Railway Deployment Configuration

## Backend Service (already deployed)
- **URL**: https://teamwellnesscompanysite-production.up.railway.app
- **Status**: ✅ Running with Google, Apple, and X OAuth

## Frontend Service (to be deployed)
- **Build Command**: `npm run build`
- **Start Command**: `npm run start`
- **Port**: 3000
- **Health Check**: `/`

## Environment Variables Added to Railway:
- ✅ GOOGLE_CLIENT_ID
- ✅ GOOGLE_CLIENT_SECRET  
- ✅ APPLE_SERVICE_ID
- ✅ APPLE_TEAM_ID
- ✅ APPLE_KEY_ID
- ✅ APPLE_PRIVATE_KEY
- ✅ TWITTER_CLIENT_ID *(newly added)*
- ✅ TWITTER_CLIENT_SECRET *(newly added)*

## Domain Migration Plan:
1. Deploy frontend to Railway
2. Configure custom domain: www.teamwellnesscompany.com
3. Update DNS from Squarespace to Railway
4. Set up SSL certificates

## Next Steps:
1. Create new service in Railway for frontend
2. Connect this repository to the new service
3. Configure custom domain
4. Update DNS records