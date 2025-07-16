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

## 2. 💳 Payment Processing (Stripe)

**Service**: Stripe Payment Processing
**Purpose**: Membership plans, wellness packages, payment history
**Where to get**:
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Create account or sign in
3. Navigate to "Developers" → "API keys"
4. Copy both Publishable key and Secret key
5. For webhooks: Go to "Developers" → "Webhooks" and create endpoint

**Environment Variables**:
- `STRIPE_SECRET_KEY` (Backend)
- `STRIPE_PUBLISHABLE_KEY` (Frontend - if needed)
- `STRIPE_WEBHOOK_SECRET` (Backend)

**Add to**: `/app/backend/.env`
```
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

## 3. 🍎 Apple Pay Integration

**Service**: Apple Pay
**Purpose**: iOS payment processing
**Where to get**:
1. Enroll in Apple Developer Program
2. Create Merchant ID in Apple Developer Console
3. Generate Payment Processing Certificate
4. Configure with Stripe (if using Stripe for Apple Pay)

**Note**: This requires Apple Developer account ($99/year)

## 4. 🔐 OAuth Authentication

### Google OAuth
**Service**: Google OAuth
**Purpose**: "Sign in with Google" functionality
**Where to get**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project or select existing
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
5. Configure authorized redirect URIs

**Environment Variables**:
```
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

### Apple OAuth
**Service**: Apple Sign In
**Purpose**: "Sign in with Apple" functionality
**Where to get**:
1. Apple Developer Account required
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

## 🚀 How to Add API Keys

1. **Edit Backend Environment File**:
   ```bash
   nano /app/backend/.env
   ```

2. **Add your keys** (example format):
   ```
   GEMINI_API_KEY=your_actual_key_here
   STRIPE_SECRET_KEY=sk_test_your_actual_key_here
   GOOGLE_CLIENT_ID=your_actual_client_id_here
   # ... add other keys
   ```

3. **Restart Backend Service**:
   ```bash
   sudo supervisorctl restart backend
   ```

4. **Frontend Keys** (if needed):
   - Create `/app/.env` file for frontend-specific keys
   - Add keys prefixed with `VITE_` for Vite access

## 💡 Current Status

**✅ Working without keys (mocked)**:
- Basic authentication
- Core program functionality
- AI chat (with placeholder responses)
- Payment structure (without actual processing)

**❌ Needs keys to work fully**:
- Actual AI responses from Gemini
- Real payment processing
- OAuth sign-in (Google, Apple)
- Email notifications

## 🔧 Development vs Production Keys

**Development** (for testing):
- Use test/sandbox keys (e.g., `sk_test_` for Stripe)
- Enable development mode in OAuth apps
- Use development endpoints

**Production** (for live app):
- Use live/production keys (e.g., `sk_live_` for Stripe)
- Configure production OAuth redirect URIs
- Use production endpoints

## 📞 Need Help?

If you need assistance obtaining any of these keys or have questions about the setup process, please let me know! I can provide more detailed instructions for any specific service.

## 🎯 Next Steps

1. **Priority 1**: Get Gemini API key for AI functionality
2. **Priority 2**: Get Stripe keys for payment processing
3. **Priority 3**: Set up Google OAuth for authentication
4. **Priority 4**: Configure other services as needed

Once you have the keys, I'll help you integrate them into the application!