import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Button from '../common/Button';
import { 
  Trophy, 
  Target, 
  Calendar, 
  Award, 
  CheckCircle,
  Clock,
  Users,
  Star,
  Gift,
  Zap
} from 'lucide-react';

const Challenges = () => {
  const [activeTab, setActiveTab] = useState('daily');

  const dailyChallenges = [
    {
      id: 1,
      title: 'Stretch 5 minutes today',
      description: 'Complete any stretch routine from our library',
      points: 50,
      completed: false,
      progress: 0,
      target: 1,
      icon: Target,
      color: 'bg-green-500'
    },
    {
      id: 2,
      title: 'Log a deep breath session',
      description: 'Practice breathing exercises for stress relief',
      points: 30,
      completed: false,
      progress: 0,
      target: 1,
      icon: Clock,
      color: 'bg-blue-500'
    },
    {
      id: 3,
      title: 'Complete a wellness check-in',
      description: 'Track your mood and energy levels',
      points: 25,
      completed: true,
      progress: 1,
      target: 1,
      icon: CheckCircle,
      color: 'bg-purple-500'
    }
  ];

  const weeklyChallenges = [
    {
      id: 4,
      title: 'Week-long wellness streak',
      description: 'Complete daily activities for 7 days in a row',
      points: 200,
      completed: false,
      progress: 3,
      target: 7,
      icon: Trophy,
      color: 'bg-orange-500'
    },
    {
      id: 5,
      title: 'Try 3 new programs',
      description: 'Explore different wellness categories',
      points: 150,
      completed: false,
      progress: 1,
      target: 3,
      icon: Star,
      color: 'bg-pink-500'
    }
  ];

  const leaderboard = [
    { id: 1, name: 'Sarah Johnson', points: 2450, rank: 1, avatar: '/api/placeholder/40/40' },
    { id: 2, name: 'Mike Chen', points: 2380, rank: 2, avatar: '/api/placeholder/40/40' },
    { id: 3, name: 'Emma Wilson', points: 2310, rank: 3, avatar: '/api/placeholder/40/40' },
    { id: 4, name: 'Alex Rodriguez', points: 2280, rank: 4, avatar: '/api/placeholder/40/40' },
    { id: 5, name: 'You', points: 2250, rank: 5, avatar: '/api/placeholder/40/40', isUser: true }
  ];

  const rewards = [
    {
      id: 1,
      name: 'Recovery Session',
      description: 'Free 30-minute session with a coach',
      cost: 500,
      icon: Users,
      color: 'bg-green-100 text-green-600'
    },
    {
      id: 2,
      name: 'Branded Wellness Mat',
      description: 'Team Welly premium yoga mat',
      cost: 800,
      icon: Gift,
      color: 'bg-blue-100 text-blue-600'
    },
    {
      id: 3,
      name: 'Team Event Credit',
      description: '$50 credit for team activities',
      cost: 1000,
      icon: Award,
      color: 'bg-purple-100 text-purple-600'
    }
  ];

  const tabs = [
    { id: 'daily', label: 'Daily Challenges', icon: Calendar },
    { id: 'weekly', label: 'Weekly Goals', icon: Trophy },
    { id: 'leaderboard', label: 'Leaderboard', icon: Users },
    { id: 'rewards', label: 'Rewards Store', icon: Gift }
  ];

  const completeChallenge = (challengeId) => {
    // Handle challenge completion
    console.log(`Challenge ${challengeId} completed!`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Team Welly Challenges</h1>
              <p className="text-sm text-gray-600">Gamify your wellness journey</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-green-50 px-3 py-1 rounded-full">
                <Award className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-700">2,250 WellyPoints</span>
              </div>
              <div className="flex items-center space-x-2 bg-orange-50 px-3 py-1 rounded-full">
                <Zap className="w-4 h-4 text-orange-600" />
                <span className="text-sm font-medium text-orange-700">3 day streak</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg mb-8 w-fit">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-white text-green-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Daily Challenges */}
        {activeTab === 'daily' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Today's Challenges</h2>
              <div className="space-y-4">
                {dailyChallenges.map((challenge) => {
                  const Icon = challenge.icon;
                  return (
                    <motion.div
                      key={challenge.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`p-4 border rounded-xl transition-all ${
                        challenge.completed
                          ? 'border-green-200 bg-green-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-center space-x-4">
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${challenge.color}`}>
                          <Icon className="w-6 h-6 text-white" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{challenge.title}</h3>
                          <p className="text-sm text-gray-600 mb-2">{challenge.description}</p>
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-1">
                              <Award className="w-4 h-4 text-yellow-500" />
                              <span className="text-sm font-medium text-gray-700">
                                {challenge.points} points
                              </span>
                            </div>
                            {challenge.completed && (
                              <div className="flex items-center space-x-1 text-green-600">
                                <CheckCircle className="w-4 h-4" />
                                <span className="text-sm font-medium">Completed</span>
                              </div>
                            )}
                          </div>
                        </div>
                        <div>
                          {challenge.completed ? (
                            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                              <CheckCircle className="w-5 h-5 text-white" />
                            </div>
                          ) : (
                            <Button
                              size="small"
                              onClick={() => completeChallenge(challenge.id)}
                            >
                              Complete
                            </Button>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Weekly Challenges */}
        {activeTab === 'weekly' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Weekly Goals</h2>
              <div className="space-y-4">
                {weeklyChallenges.map((challenge) => {
                  const Icon = challenge.icon;
                  const progressPercentage = (challenge.progress / challenge.target) * 100;
                  return (
                    <motion.div
                      key={challenge.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-4 border border-gray-200 rounded-xl hover:border-gray-300 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${challenge.color}`}>
                          <Icon className="w-6 h-6 text-white" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{challenge.title}</h3>
                          <p className="text-sm text-gray-600 mb-2">{challenge.description}</p>
                          <div className="flex items-center space-x-4 mb-2">
                            <div className="flex items-center space-x-1">
                              <Award className="w-4 h-4 text-yellow-500" />
                              <span className="text-sm font-medium text-gray-700">
                                {challenge.points} points
                              </span>
                            </div>
                            <div className="text-sm text-gray-500">
                              {challenge.progress}/{challenge.target} completed
                            </div>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-green-500 h-2 rounded-full transition-all duration-500"
                              style={{ width: `${progressPercentage}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Leaderboard */}
        {activeTab === 'leaderboard' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Company Leaderboard</h2>
              <div className="space-y-3">
                {leaderboard.map((user) => (
                  <motion.div
                    key={user.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex items-center space-x-4 p-4 rounded-xl transition-colors ${
                      user.isUser ? 'bg-green-50 border border-green-200' : 'bg-gray-50'
                    }`}
                  >
                    <div className="flex-shrink-0 w-8 text-center">
                      <span className={`font-bold ${user.rank <= 3 ? 'text-yellow-600' : 'text-gray-600'}`}>
                        #{user.rank}
                      </span>
                    </div>
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                      <Users className="w-5 h-5 text-gray-400" />
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">{user.name}</div>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Award className="w-4 h-4 text-yellow-500" />
                      <span className="font-bold text-gray-900">{user.points.toLocaleString()}</span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Rewards Store */}
        {activeTab === 'rewards' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Rewards Store</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {rewards.map((reward) => {
                  const Icon = reward.icon;
                  return (
                    <motion.div
                      key={reward.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow"
                    >
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-4 ${reward.color}`}>
                        <Icon className="w-6 h-6" />
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-2">{reward.name}</h3>
                      <p className="text-sm text-gray-600 mb-4">{reward.description}</p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-1">
                          <Award className="w-4 h-4 text-yellow-500" />
                          <span className="font-bold text-gray-900">{reward.cost}</span>
                        </div>
                        <Button size="small">
                          Redeem
                        </Button>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Challenges;