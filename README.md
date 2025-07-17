# Team Wellness Company - Landing Page Website

A professional landing page website for Team Wellness Company, featuring a modern design with sign-in and learn more functionality. The site showcases our wellness services, pricing plans, and company information with an elegant dark theme and responsive design.

## 🌟 Features

### Landing Page
- **Professional Design** with dark blue gradient theme and SensaWild-Fill font
- **Sign In Modal** with Apple, Google, and X SSO options plus traditional login
- **Learn More Modal** with comprehensive business information, pricing, and contact forms
- **Responsive Layout** optimized for all screen sizes
- **Interactive Elements** with smooth animations and hover effects

### Business Information
- **Company Mission** and founder profiles
- **Service Offerings** with detailed descriptions
- **Pricing Plans** for individual and corporate clients
- **Contact Information** with Calendly integration and email links
- **Social Media Links** and newsletter signup

### Technical Features
- **Static HTML/CSS/JavaScript** for optimal performance
- **Custom SVG Logo** with Team Welly branding
- **Modal System** for enhanced user experience
- **Responsive Design** for mobile and desktop
- **Professional Typography** with custom font integration

## 🚀 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with gradients and animations
- **Typography**: SensaWild-Fill custom font
- **Icons**: Custom SVG icons and social media icons
- **Responsive Design**: Mobile-first approach
- **Backend**: FastAPI Python (for future integration)
- **Database**: MongoDB (for future user data)

## 📱 Installation & Setup

### Prerequisites
- Modern web browser
- Local web server (optional for development)

### Development Setup
```bash
# Clone the repository
git clone https://github.com/faraon87/TeamWellnessCompanySite.git

# Navigate to project directory
cd TeamWellnessCompanySite

# Open index.html in your browser
# Or use a local web server:
python -m http.server 8000
# Then visit http://localhost:8000
```

### File Structure
```
/
├── index.html           # Main landing page
├── styles.css          # Custom CSS styling
├── fonts/              # Custom font files
│   ├── SensaWild-Fill.otf
│   └── SensaWild-Fill.ttf
├── public/             # Static assets
│   ├── background.png  # Background image
│   └── twclogo.svg     # Team Welly logo
└── README.md           # This file
```

## 🌐 Deployment

### Vercel Deployment
1. Connect your GitHub repository to Vercel
2. Configure build settings:
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. Deploy automatically on every push

### Environment Variables
No environment variables required for the current version. All data is stored locally for demo purposes.

## 🏗️ Architecture

### Component Structure
```
src/
├── components/
│   ├── common/           # Reusable UI components
│   ├── onboarding/       # User onboarding flow
│   ├── dashboard/        # Main dashboard
│   ├── programs/         # Programs library
│   ├── coaching/         # Live coaching features
│   ├── challenges/       # Gamification system
│   ├── settings/         # User settings
│   ├── admin/           # Admin portal
│   └── membership/      # Subscription plans
├── contexts/            # React Context providers
├── hooks/              # Custom React hooks
└── App.jsx             # Main application component
```

## 🎯 Key User Journeys

### New User Onboarding
1. Welcome screen with intro video
2. Goal selection (Reduce Pain, Improve Flexibility, etc.)
3. Baseline self-assessment
4. Device integration setup
5. Dashboard introduction

### Daily Wellness Routine
1. Check personalized daily suggestions
2. Complete wellness activities
3. Track progress and earn WellyPoints
4. Participate in challenges
5. Book coaching sessions

### Corporate Admin Flow
1. View employee engagement dashboard
2. Analyze wellness program ROI
3. Send targeted messages to employees
4. Customize package features
5. Generate detailed reports

## 📊 Future Backend Integration

### Required API Endpoints
- **Authentication**: `/api/auth/*` (login, register, social auth)
- **User Management**: `/api/user/*` (profile, progress, settings)
- **Programs**: `/api/programs/*` (catalog, bookmarks, completion)
- **Coaching**: `/api/coaching/*` (bookings, sessions, coaches)
- **Challenges**: `/api/challenges/*` (daily/weekly, leaderboard, rewards)
- **Admin**: `/api/admin/*` (dashboard, employees, reports)

### Database Schema
- Users, Programs, Progress, Bookings, Challenges, Companies, Admin Actions

## 🔧 Development Guidelines

### Code Style
- ES6+ JavaScript with React Hooks
- Tailwind CSS for styling
- Component-based architecture
- Responsive-first design approach

### Performance Optimization
- Lazy loading for route components
- Image optimization and placeholders
- Progressive Web App caching
- Efficient state management

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For support, please contact the development team or create an issue in the repository.

---

**Team Welly - Making wellness accessible, engaging, and effective for everyone! 🌱**
