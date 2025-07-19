# Domain Migration Guide: www.teamwellnesscompany.com

## Current Status
- ✅ **Frontend**: https://twc-website-front-end-production.up.railway.app
- ✅ **Backend**: https://teamwellnesscompanysite-production.up.railway.app
- ❌ **Custom Domain**: www.teamwellnesscompany.com (currently on Squarespace)

## Migration Steps

### Phase 1: Railway Domain Configuration

#### Frontend Service (www.teamwellnesscompany.com)
1. **Railway Dashboard** → Frontend Service → **Settings** → **Domains**
2. **Add Custom Domain**: `www.teamwellnesscompany.com`
3. **Railway will provide**: DNS records to configure

#### Backend Service (api.teamwellnesscompany.com)
1. **Railway Dashboard** → Backend Service → **Settings** → **Domains**
2. **Add Custom Domain**: `api.teamwellnesscompany.com`
3. **Update Environment Variables**: Update CORS and allowed origins

### Phase 2: DNS Configuration

#### Update DNS Records (in your domain registrar):
```
Type: CNAME
Name: www
Value: [Railway-provided-value]

Type: CNAME  
Name: api
Value: [Railway-provided-value]
```

#### Update Frontend Environment Variable:
```
VITE_API_URL=https://api.teamwellnesscompany.com
```

### Phase 3: OAuth Provider Updates

#### Google OAuth Console:
- Add: `https://api.teamwellnesscompany.com/api/auth/google/callback`
- Add: `https://www.teamwellnesscompany.com`

#### Apple Developer Console:
- Update redirect URI: `https://api.teamwellnesscompany.com/api/auth/apple/callback`
- Update domain: `www.teamwellnesscompany.com`

#### Twitter Developer Console:
- Update redirect URI: `https://api.teamwellnesscompany.com/api/auth/twitter/callback`
- Update domain: `www.teamwellnesscompany.com`

### Phase 4: SSL & Security
- ✅ **Railway Auto-SSL**: Automatically provisions SSL certificates
- ✅ **HTTPS Redirect**: Automatic HTTPS enforcement
- ✅ **Security Headers**: Configure security headers for production

### Phase 5: Testing After Migration
1. **Test Custom Domain**: Verify www.teamwellnesscompany.com loads properly
2. **Test OAuth Flows**: All providers work with custom domain
3. **Test Performance**: Ensure fast loading and responsiveness
4. **Test Mobile**: Verify mobile experience on custom domain

## Migration Timeline
- **Immediate**: Update Google OAuth for Railway URLs
- **When Ready**: Configure custom domains in Railway
- **After DNS**: Update OAuth providers for custom domains
- **Final**: Complete testing on custom domain

## Current Application Status
✅ **Fully Functional**: Application working perfectly on Railway URLs
✅ **Production Ready**: All features tested and operational
✅ **OAuth Integration**: Apple and Twitter/X working, Google needs URL update
✅ **Responsive Design**: Professional experience across all devices