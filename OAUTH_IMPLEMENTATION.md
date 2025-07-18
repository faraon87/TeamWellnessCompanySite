# OAuth Implementation Documentation

## Overview
This project includes OAuth SSO implementation with support for Google, Apple, and Twitter/X authentication.

## Backend Implementation
- **OAuth Router**: `/app/backend/app/routers/oauth.py`
- **Google OAuth**: Fully implemented with real credentials (configured via environment variables)
- **Apple & Twitter**: Placeholder structures ready for credentials

## Frontend Integration
- Google OAuth button connects to backend endpoints
- Automatic token storage and user redirect
- Error handling for failed authentication

## Environment Variables Required
```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Setup for Production
1. Set environment variables in your hosting platform
2. Configure OAuth redirect URIs in Google Cloud Console
3. Test the authentication flow

## Security Notes
- Never commit real credentials to version control
- Use environment variables for sensitive data
- Separate credentials for development and production

## Files Structure
- `backend/.env` - Placeholder credentials (safe to commit)
- `backend/.env.local` - Real credentials (ignored by git)
- `backend/app/routers/oauth.py` - OAuth implementation
- Frontend integration in `index.html`