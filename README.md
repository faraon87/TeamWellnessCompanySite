# Team Welly - Health & Wellness App

A comprehensive health and wellness platform designed for individual and corporate users, offering an intuitive and engaging user experience with personalized programs, live coaching, gamification, and admin portal.

## 🌟 Features

### For Users
- **Personalized Dashboard** with daily suggestions and progress tracking
- **Wellness Programs Library** with 6+ categories (Stretch & Mobility, Pain to Performance, etc.)
- **Live Coaching** with 1-on-1 sessions and group workshops
- **Gamification System** with challenges, leaderboards, and rewards
- **Progress Tracking** with visual progress rings and analytics
- **Device Integration** support for Apple Health, Fitbit, and Garmin

### For Administrators
- **Corporate Dashboard** with employee engagement metrics
- **ROI Reports** showing wellness program impact
- **Employee Messaging** system for tips and announcements
- **Package Customization** for corporate clients

### Technical Features
- **Progressive Web App (PWA)** with offline support
- **Responsive Design** optimized for mobile and desktop
- **iOS-optimized** user experience
- **Real-time Notifications** and updates
- **Secure Authentication** with social login options

## 🚀 Tech Stack

- **Frontend**: React 18.2.0 + Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **State Management**: React Context API
- **Routing**: React Router
- **PWA**: Service Worker + Web App Manifest

## 📱 Installation & Setup

### Prerequisites
- Node.js 16+ and npm
- Modern web browser

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/team-welly-app.git

# Navigate to project directory
cd team-welly-app

# Install dependencies
npm install

# Start development server
npm run dev
```

### Production Build
```bash
# Build for production
npm run build

# Preview production build
npm run preview
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
