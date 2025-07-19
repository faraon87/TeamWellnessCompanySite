import React from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../hooks/useAuth';
import { useApp } from '../../contexts/AppContext';
import ProgressRing from '../common/ProgressRing';
import Button from '../common/Button';
import { 
  Play, 
  Calendar, 
  Award, 
  TrendingUp, 
  Heart, 
  Activity,
  Clock,
  Star
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const { state } = useApp();

  const todayProgress = {
    daily: 75,
    weekly: 60,
    monthly: 45
  };

  const suggestions = [
    {
      id: 1,
      title: 'Morning Neck & Shoulder Stretch',
      type: 'Stretch',
      duration: '5 min',
      thumbnail: '/api/placeholder/200/150',
      completed: false
    },
    {
      id: 2,
      title: 'Box Breathing for Focus',
      type: 'Breathwork',
      duration: '3 min',
      thumbnail: '/api/placeholder/200/150',
      completed: false
    },
    {
      id: 3,
      title: 'Mindful Moment',
      type: 'Meditation',
      duration: '7 min',
      thumbnail: '/api/placeholder/200/150',
      completed: false
    }
  ];

  const upcomingBookings = [
    {
      id: 1,
      title: 'Recovery Session with Chris',
      type: '1-on-1 Coaching',
      time: 'Today, 2:00 PM',
      coach: 'Chris Thompson'
    },
    {
      id: 2,
      title: 'Workplace Wellness Workshop',
      type: 'Group Session',
      time: 'Tomorrow, 10:00 AM',
      coach: 'Fran Martinez'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Good morning, {user?.name}! 👋
              </h1>
              <p className="text-sm text-gray-600">
                Ready to make today amazing?
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-green-50 px-3 py-1 rounded-full">
                <Award className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-700">
                  {state.userProgress.wellyPoints} WellyPoints
                </span>
              </div>
              <div className="flex items-center space-x-2 bg-orange-50 px-3 py-1 rounded-full">
                <TrendingUp className="w-4 h-4 text-orange-600" />
                <span className="text-sm font-medium text-orange-700">
                  {state.userProgress.currentStreak} day streak
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Today's Suggestions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl shadow-sm p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Today's Suggestions
                </h2>
                <Button variant="ghost" size="small">
                  View All
                </Button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {suggestions.map((suggestion) => (
                  <div
                    key={suggestion.id}
                    className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="aspect-video bg-gray-200 rounded-lg mb-3 flex items-center justify-center">
                      <Play className="w-8 h-8 text-gray-400" />
                    </div>
                    <h3 className="font-medium text-gray-900 mb-1">
                      {suggestion.title}
                    </h3>
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <span>{suggestion.type}</span>
                      <span className="flex items-center">
                        <Clock className="w-3 h-3 mr-1" />
                        {suggestion.duration}
                      </span>
                    </div>
                    <Button
                      size="small"
                      fullWidth
                      className="mt-3"
                      icon={Play}
                      iconPosition="left"
                    >
                      Start Now
                    </Button>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Upcoming Bookings */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl shadow-sm p-6"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Upcoming Sessions
              </h2>
              
              <div className="space-y-4">
                {upcomingBookings.map((booking) => (
                  <div
                    key={booking.id}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-xl"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <Calendar className="w-6 h-6 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900">
                          {booking.title}
                        </h3>
                        <p className="text-sm text-gray-500">
                          {booking.type} • {booking.time}
                        </p>
                        <p className="text-xs text-gray-400">
                          with {booking.coach}
                        </p>
                      </div>
                    </div>
                    <Button variant="outline" size="small">
                      Join
                    </Button>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Right Column - Progress & Stats */}
          <div className="space-y-8">
            {/* Progress Rings */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl shadow-sm p-6"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Progress Overview
              </h2>
              
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">Daily Goals</h3>
                    <p className="text-sm text-gray-500">3 of 4 completed</p>
                  </div>
                  <ProgressRing
                    progress={todayProgress.daily}
                    size={80}
                    color="#059669"
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">Weekly Trend</h3>
                    <p className="text-sm text-gray-500">Above average</p>
                  </div>
                  <ProgressRing
                    progress={todayProgress.weekly}
                    size={80}
                    color="#3b82f6"
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">Monthly</h3>
                    <p className="text-sm text-gray-500">Keep it up!</p>
                  </div>
                  <ProgressRing
                    progress={todayProgress.monthly}
                    size={80}
                    color="#f59e0b"
                  />
                </div>
              </div>
            </motion.div>

            {/* Quick Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-2xl shadow-sm p-6"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Quick Stats
              </h2>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <Heart className="w-4 h-4 text-green-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-900">
                      Programs Completed
                    </span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">12</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <Activity className="w-4 h-4 text-blue-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-900">
                      Total Sessions
                    </span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">45</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                      <Star className="w-4 h-4 text-yellow-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-900">
                      Badges Earned
                    </span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">8</span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;