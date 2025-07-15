import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Button from '../common/Button';
import { 
  Calendar, 
  Clock, 
  Users, 
  Video, 
  MessageSquare, 
  Star,
  User,
  PlayCircle,
  Plus
} from 'lucide-react';

const LiveCoaching = () => {
  const [activeTab, setActiveTab] = useState('1on1');

  const coaches = [
    {
      id: 1,
      name: 'Chris Thompson',
      specialty: 'Recovery & Pain Management',
      rating: 4.9,
      experience: '8 years',
      avatar: '/api/placeholder/100/100',
      nextAvailable: 'Today, 2:00 PM',
      bio: 'Specializes in helping clients overcome chronic pain and improve mobility.'
    },
    {
      id: 2,
      name: 'Fran Martinez',
      specialty: 'Wellness Strategy',
      rating: 4.8,
      experience: '6 years',
      avatar: '/api/placeholder/100/100',
      nextAvailable: 'Tomorrow, 9:00 AM',
      bio: 'Expert in developing comprehensive wellness strategies for individuals and teams.'
    }
  ];

  const groupSessions = [
    {
      id: 1,
      title: 'Workplace Wellness Workshop',
      date: 'March 15, 2025',
      time: '10:00 AM - 11:00 AM',
      coach: 'Fran Martinez',
      participants: 24,
      maxParticipants: 30,
      thumbnail: '/api/placeholder/300/200',
      description: 'Learn practical wellness strategies for the modern workplace'
    },
    {
      id: 2,
      title: 'Stress Management Masterclass',
      date: 'March 18, 2025',
      time: '2:00 PM - 3:30 PM',
      coach: 'Chris Thompson',
      participants: 18,
      maxParticipants: 25,
      thumbnail: '/api/placeholder/300/200',
      description: 'Master techniques for managing stress and building resilience'
    }
  ];

  const replayLibrary = [
    {
      id: 1,
      title: 'Building Healthy Habits',
      date: 'March 10, 2025',
      coach: 'Fran Martinez',
      duration: '45 min',
      views: 156,
      thumbnail: '/api/placeholder/300/200'
    },
    {
      id: 2,
      title: 'Desk Stretches for Remote Workers',
      date: 'March 8, 2025',
      coach: 'Chris Thompson',
      duration: '30 min',
      views: 203,
      thumbnail: '/api/placeholder/300/200'
    }
  ];

  const tabs = [
    { id: '1on1', label: '1-on-1 Sessions', icon: User },
    { id: 'group', label: 'Group Sessions', icon: Users },
    { id: 'replay', label: 'Replay Library', icon: PlayCircle }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Live Coaching</h1>
              <p className="text-sm text-gray-600">Connect with wellness experts</p>
            </div>
            <Button icon={MessageSquare} iconPosition="left">
              Request Custom Topic
            </Button>
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

        {/* 1-on-1 Sessions */}
        {activeTab === '1on1' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Our Coaches</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {coaches.map((coach) => (
                  <motion.div
                    key={coach.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start space-x-4">
                      <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center">
                        <User className="w-8 h-8 text-gray-400" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{coach.name}</h3>
                        <p className="text-sm text-gray-600 mb-2">{coach.specialty}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                          <div className="flex items-center space-x-1">
                            <Star className="w-4 h-4 text-yellow-400 fill-current" />
                            <span>{coach.rating}</span>
                          </div>
                          <span>{coach.experience}</span>
                        </div>
                        <p className="text-sm text-gray-600 mb-4">{coach.bio}</p>
                        <div className="flex items-center justify-between">
                          <div className="text-sm text-gray-500">
                            Next available: {coach.nextAvailable}
                          </div>
                          <Button size="small" icon={Calendar}>
                            Book Session
                          </Button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Group Sessions */}
        {activeTab === 'group' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Upcoming Group Sessions</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {groupSessions.map((session) => (
                  <motion.div
                    key={session.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow"
                  >
                    <div className="aspect-video bg-gray-200 flex items-center justify-center">
                      <Video className="w-12 h-12 text-gray-400" />
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-gray-900 mb-2">{session.title}</h3>
                      <p className="text-sm text-gray-600 mb-3">{session.description}</p>
                      <div className="space-y-2 text-sm text-gray-500 mb-4">
                        <div className="flex items-center space-x-2">
                          <Calendar className="w-4 h-4" />
                          <span>{session.date}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Clock className="w-4 h-4" />
                          <span>{session.time}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Users className="w-4 h-4" />
                          <span>{session.participants}/{session.maxParticipants} participants</span>
                        </div>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="text-sm text-gray-500">
                          with {session.coach}
                        </div>
                        <Button size="small" icon={Plus}>
                          Register
                        </Button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Replay Library */}
        {activeTab === 'replay' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Session Replays</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {replayLibrary.map((replay) => (
                  <motion.div
                    key={replay.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow"
                  >
                    <div className="relative">
                      <div className="aspect-video bg-gray-200 flex items-center justify-center">
                        <PlayCircle className="w-12 h-12 text-gray-400" />
                      </div>
                      <div className="absolute bottom-2 right-2 bg-black/60 text-white px-2 py-1 rounded text-xs">
                        {replay.duration}
                      </div>
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-gray-900 mb-2">{replay.title}</h3>
                      <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
                        <span>{replay.date}</span>
                        <span>{replay.views} views</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="text-sm text-gray-500">
                          with {replay.coach}
                        </div>
                        <Button size="small" icon={PlayCircle}>
                          Watch
                        </Button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LiveCoaching;