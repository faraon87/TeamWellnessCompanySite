# API Keys and Third-Party Integration Setup

## 🔑 Required API Keys for Team Welly App

To enable full functionality of the Team Welly app, you'll need to obtain API keys for the following services:

## 1. 🤖 AI Chatbot Integration (Gemini 2.0-flash)

**Service**: Google Gemini AI
**Purpose**: AI-powered wellness coaching and behavior analysis
**Where to get**:
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new project or select an existing one
4. Go to "Get API key" section
5. Generate a new API key

**Environment Variable**: `GEMINI_API_KEY`
**Add to**: `/app/backend/.env`

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## 2. 💳 Payment Processing (Stripe) - VERIFIED INTEGRATION

**Service**: Stripe Payment Processing
**Purpose**: Membership plans, wellness packages, payment history
**Integration Status**: ✅ VERIFIED PLAYBOOK Available

**IMPORTANT**: Stripe integration is already configured to use system environment variables. No manual setup required for development.

For production, you'll need:
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Create account or sign in
3. Navigate to "Developers" → "API keys"
4. Copy both Publishable key and Secret key
5. For webhooks: Go to "Developers" → "Webhooks" and create endpoint

**Environment Variables** (Production only):
```
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

## 3. 🔐 Authentication Integration - VERIFIED INTEGRATION

**Service**: Emergent Auth (Google OAuth Alternative)
**Purpose**: Hassle-free email-based authentication
**Integration Status**: ✅ VERIFIED PLAYBOOK Available

**IMPORTANT**: This integration uses Emergent's authentication system - no additional API keys needed!

**How it works**:
1. User clicks "Sign in with Google" → Redirects to `https://auth.emergentagent.com/`
2. After login → Redirects back with session ID
3. Backend calls Emergent Auth API to validate session
4. User data automatically stored in database

**No manual setup required** - this integration is ready to use!

## 4. 📱 Apple Sign In (Optional)

**Service**: Apple Sign In
**Purpose**: "Sign in with Apple" functionality
**Where to get**:
1. Apple Developer Account required ($99/year)
2. Create App ID with Sign In with Apple capability
3. Create Service ID for web authentication
4. Generate private key for client authentication

**Environment Variables**:
```
APPLE_CLIENT_ID=your_apple_client_id_here
APPLE_TEAM_ID=your_apple_team_id_here
APPLE_KEY_ID=your_apple_key_id_here
APPLE_PRIVATE_KEY=your_apple_private_key_here
```

## 5. 📧 Email Service (Optional)

**Service**: SendGrid or similar
**Purpose**: User notifications, password reset, etc.
**Where to get**:
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Verify sender identity
3. Create API key in Settings → API Keys

**Environment Variables**:
```
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=your_verified_sender_email_here
```

## 🚀 Integration Status Summary

| Service | Status | Setup Required |
|---------|--------|----------------|
| **AI Chatbot (Gemini)** | ⚠️ Needs API Key | Manual setup required |
| **Payments (Stripe)** | ✅ Ready | Auto-configured for dev |
| **Authentication (Emergent)** | ✅ Ready | No setup needed |
| **Apple Sign In** | ⚠️ Optional | Manual setup required |
| **Email Service** | ⚠️ Optional | Manual setup required |

## 🛠️ Quick Setup Instructions

### For Development (Minimum Required):
1. **Get Gemini API Key** (only required key):
   ```bash
   echo "GEMINI_API_KEY=your_key_here" >> /app/backend/.env
   sudo supervisorctl restart backend
   ```

2. **Test the integrations**:
   - Authentication: Already working with Emergent Auth
   - Payments: Already configured with Stripe
   - AI Chat: Will work once Gemini key is added

### For Production:
1. Add Gemini API key (required)
2. Add production Stripe keys (recommended)
3. Add Apple Sign In credentials (optional)
4. Add email service credentials (optional)

## 💡 Current Status Without Keys

**✅ Working immediately**:
- User registration and login
- Basic authentication flow
- Payment integration structure
- AI chat interface (with placeholder responses)
- Dashboard and program management

**❌ Needs API keys to work fully**:
- Actual AI responses from Gemini
- Production payment processing
- Apple Sign In authentication
- Email notifications

## 🔧 Development vs Production

**Development Mode** (current):
- Uses Emergent Auth for authentication ✅
- Uses system Stripe keys for payments ✅
- Uses placeholder AI responses ⚠️
- Core functionality working ✅

**Production Mode**:
- Add your own Stripe production keys
- Add Gemini API key for AI functionality
- Add Apple Sign In for iOS users
- Add email service for notifications

## 🎯 Priority Setup Order

1. **High Priority**: Get Gemini API key for AI functionality
2. **Medium Priority**: Set up production Stripe keys
3. **Low Priority**: Add Apple Sign In and email service

## 📞 Need Help?

The integrations are designed to work out-of-the-box with minimal setup. Most functionality is already available, and you only need to add the Gemini API key for full AI functionality.

**Ready to use immediately**: Authentication, payments, dashboard, programs
**Needs Gemini key**: AI-powered wellness coaching and behavior analysis