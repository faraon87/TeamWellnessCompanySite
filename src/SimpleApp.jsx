import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { Heart, Target, Home, BookOpen, Users, Trophy, Settings, Play, Calendar, Award, User, Filter, Search, Clock, Star, TrendingUp, Activity, CheckCircle, Send, BarChart3, MessageSquare, Bell, Shield, HelpCircle, CreditCard, Apple } from 'lucide-react';

// Simple Button Component
const Button = ({ children, onClick, className = "", variant = "primary", fullWidth = false, icon: Icon, loading = false }) => {
  const baseClass = "px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2";
  const variants = {
    primary: "bg-green-600 hover:bg-green-700 text-white",
    secondary: "bg-gray-600 hover:bg-gray-700 text-white",
    outline: "border-2 border-green-600 text-green-600 hover:bg-green-50"
  };
  
  return (
    <button
      onClick={onClick}
      className={`${baseClass} ${variants[variant]} ${fullWidth ? 'w-full' : ''} ${className}`}
      disabled={loading}
    >
      {loading ? (
        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
      ) : (
        <>
          {Icon && <Icon className="w-4 h-4" />}
          <span>{children}</span>
        </>
      )}
    </button>
  );
};

// Welcome Screen
const WelcomeScreen = ({ onComplete }) => {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleStart = () => {
    setIsLoading(true);
    // Simulate onboarding process
    setTimeout(() => {
      onComplete();
    }, 1000);
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
        <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <Heart className="w-8 h-8 text-white" />
        </div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome to Team Welly
        </h1>
        
        <p className="text-gray-600 mb-8">
          Your comprehensive health and wellness companion. Let's get you started on your journey to better health.
        </p>
        
        <Button
          fullWidth
          onClick={handleStart}
          icon={Target}
          loading={isLoading}
        >
          {isLoading ? 'Setting up...' : 'Start Your Wellness Journey'}
        </Button>
        
        <div className="mt-8 text-xs text-gray-400">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </div>
      </div>
    </div>
  );
};

// Dashboard Component
const Dashboard = () => {
  const suggestions = [
    { id: 1, title: 'Morning Neck & Shoulder Stretch', type: 'Stretch', duration: '5 min' },
    { id: 2, title: 'Box Breathing for Focus', type: 'Breathwork', duration: '3 min' },
    { id: 3, title: 'Mindful Moment', type: 'Meditation', duration: '7 min' }
  ];

  const upcomingBookings = [
    { id: 1, title: 'Recovery Session with Chris', time: 'Today, 2:00 PM' },
    { id: 2, title: 'Workplace Wellness Workshop', time: 'Tomorrow, 10:00 AM' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Good morning! 👋</h1>
              <p className="text-sm text-gray-600">Ready to make today amazing?</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-green-50 px-3 py-1 rounded-full">
                <Award className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-700">2,250 WellyPoints</span>
              </div>
              <div className="flex items-center space-x-2 bg-orange-50 px-3 py-1 rounded-full">
                <TrendingUp className="w-4 h-4 text-orange-600" />
                <span className="text-sm font-medium text-orange-700">3 day streak</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Today's Suggestions */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-sm p-6 mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Today's Suggestions</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {suggestions.map((suggestion) => (
                  <div key={suggestion.id} className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4">
                    <div className="aspect-video bg-gray-200 rounded-lg mb-3 flex items-center justify-center">
                      <Play className="w-8 h-8 text-gray-400" />
                    </div>
                    <h3 className="font-medium text-gray-900 mb-1">{suggestion.title}</h3>
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <span>{suggestion.type}</span>
                      <span className="flex items-center">
                        <Clock className="w-3 h-3 mr-1" />
                        {suggestion.duration}
                      </span>
                    </div>
                    <Button className="mt-3" fullWidth icon={Play}>
                      Start Now
                    </Button>
                  </div>
                ))}
              </div>
            </div>

            {/* Upcoming Bookings */}
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Upcoming Sessions</h2>
              <div className="space-y-4">
                {upcomingBookings.map((booking) => (
                  <div key={booking.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <Calendar className="w-6 h-6 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900">{booking.title}</h3>
                        <p className="text-sm text-gray-500">{booking.time}</p>
                      </div>
                    </div>
                    <Button variant="outline">Join</Button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Progress Stats */}
          <div className="space-y-8">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Progress Overview</h2>
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">Daily Goals</h3>
                    <p className="text-sm text-gray-500">3 of 4 completed</p>
                  </div>
                  <div className="w-16 h-16 relative">
                    <div className="w-full h-full bg-gray-200 rounded-full"></div>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-sm font-bold text-gray-900">75%</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">Weekly Trend</h3>
                    <p className="text-sm text-gray-500">Above average</p>
                  </div>
                  <div className="w-16 h-16 relative">
                    <div className="w-full h-full bg-gray-200 rounded-full"></div>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-sm font-bold text-gray-900">60%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Stats</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <Heart className="w-4 h-4 text-green-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-900">Programs Completed</span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">12</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <Activity className="w-4 h-4 text-blue-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-900">Total Sessions</span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">45</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                      <Star className="w-4 h-4 text-yellow-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-900">Badges Earned</span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">8</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Navigation Component
const Navigation = ({ currentPage, onPageChange }) => {
  const navigationItems = [
    { id: 'dashboard', icon: Home, label: 'Dashboard' },
    { id: 'programs', icon: BookOpen, label: 'Programs' },
    { id: 'coaching', icon: Users, label: 'Coaching' },
    { id: 'challenges', icon: Trophy, label: 'Challenges' },
    { id: 'settings', icon: Settings, label: 'Settings' }
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-2 py-1 md:hidden">
      <div className="flex justify-around">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={`flex flex-col items-center py-2 px-3 min-w-0 flex-1 text-center transition-colors ${
                currentPage === item.id ? 'text-green-600' : 'text-gray-500'
              }`}
            >
              <Icon className="h-5 w-5" />
              <span className="text-xs mt-1 truncate">{item.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

// Simple Programs Component
const Programs = () => (
  <div className="min-h-screen bg-gray-50 p-4">
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Programs Library</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {['Stretch & Mobility', 'Pain to Performance', 'Strength Foundations', 'Breath & Stress', 'Workplace Wellness', 'Mindset & Growth'].map((category) => (
          <div key={category} className="bg-white rounded-2xl shadow-sm p-6">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <BookOpen className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">{category}</h3>
            <p className="text-sm text-gray-600 mb-4">Discover wellness programs tailored for you</p>
            <Button variant="outline" fullWidth>Explore</Button>
          </div>
        ))}
      </div>
    </div>
  </div>
);

// Main App Component
const TeamWellyApp = () => {
  const [isOnboarded, setIsOnboarded] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard');

  if (!isOnboarded) {
    return <WelcomeScreen onComplete={() => setIsOnboarded(true)} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {currentPage === 'dashboard' && <Dashboard />}
      {currentPage === 'programs' && <Programs />}
      {currentPage !== 'dashboard' && currentPage !== 'programs' && (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              {currentPage.charAt(0).toUpperCase() + currentPage.slice(1)}
            </h2>
            <p className="text-gray-600">This section is coming soon!</p>
          </div>
        </div>
      )}
      <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
    </div>
  );
};

export default TeamWellyApp;