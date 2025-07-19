import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Button from '../common/Button';
import { 
  Search, 
  Filter, 
  Play, 
  Heart, 
  Clock, 
  Star,
  BookOpen,
  Users,
  Target,
  Brain,
  Zap,
  Activity
} from 'lucide-react';

const ProgramsLibrary = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    { id: 'all', name: 'All Programs', icon: BookOpen, color: 'text-gray-600' },
    { id: 'stretch', name: 'Stretch & Mobility', icon: Activity, color: 'text-green-600' },
    { id: 'pain', name: 'Pain to Performance', icon: Target, color: 'text-red-600' },
    { id: 'strength', name: 'Strength Foundations', icon: Zap, color: 'text-orange-600' },
    { id: 'breath', name: 'Breath & Stress', icon: Brain, color: 'text-blue-600' },
    { id: 'workplace', name: 'Workplace Wellness', icon: Users, color: 'text-purple-600' },
    { id: 'mindset', name: 'Mindset & Growth', icon: Star, color: 'text-pink-600' }
  ];

  const programs = [
    {
      id: 1,
      title: 'Full Body Morning Stretch',
      category: 'stretch',
      duration: '15 min',
      level: 'Beginner',
      rating: 4.8,
      thumbnail: '/api/placeholder/300/200',
      description: 'Wake up your body with gentle stretches',
      instructor: 'Sarah Johnson',
      completions: 1204
    },
    {
      id: 2,
      title: 'Neck & Shoulder Relief',
      category: 'pain',
      duration: '10 min',
      level: 'All Levels',
      rating: 4.9,
      thumbnail: '/api/placeholder/300/200',
      description: 'Target tension in your neck and shoulders',
      instructor: 'Mike Chen',
      completions: 2156
    },
    {
      id: 3,
      title: 'Core Stability Foundation',
      category: 'strength',
      duration: '20 min',
      level: 'Intermediate',
      rating: 4.7,
      thumbnail: '/api/placeholder/300/200',
      description: 'Build a strong foundation with core exercises',
      instructor: 'Alex Rodriguez',
      completions: 892
    },
    {
      id: 4,
      title: 'Box Breathing Mastery',
      category: 'breath',
      duration: '8 min',
      level: 'Beginner',
      rating: 4.9,
      thumbnail: '/api/placeholder/300/200',
      description: 'Master the art of controlled breathing',
      instructor: 'Emma Wilson',
      completions: 3247
    },
    {
      id: 5,
      title: 'Desk Warrior Routine',
      category: 'workplace',
      duration: '12 min',
      level: 'All Levels',
      rating: 4.8,
      thumbnail: '/api/placeholder/300/200',
      description: 'Perfect for office workers and remote teams',
      instructor: 'David Kim',
      completions: 1678
    },
    {
      id: 6,
      title: 'Confidence Building Meditation',
      category: 'mindset',
      duration: '15 min',
      level: 'Beginner',
      rating: 4.6,
      thumbnail: '/api/placeholder/300/200',
      description: 'Build inner confidence and self-belief',
      instructor: 'Lisa Thompson',
      completions: 965
    }
  ];

  const filteredPrograms = programs.filter(program => {
    const matchesCategory = selectedCategory === 'all' || program.category === selectedCategory;
    const matchesSearch = program.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         program.instructor.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Programs Library</h1>
              <p className="text-sm text-gray-600">Discover wellness programs tailored for you</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search programs..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              <Button variant="outline" size="small" icon={Filter}>
                Filter
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Category Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Categories</h2>
              <div className="space-y-2">
                {categories.map((category) => {
                  const Icon = category.icon;
                  return (
                    <button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id)}
                      className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                        selectedCategory === category.id
                          ? 'bg-green-50 text-green-700 border-r-2 border-green-500'
                          : 'text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className={`w-5 h-5 ${selectedCategory === category.id ? category.color : 'text-gray-400'}`} />
                      <span className="text-sm font-medium">{category.name}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Programs Grid */}
          <div className="flex-1">
            <div className="mb-6">
              <p className="text-sm text-gray-600">
                {filteredPrograms.length} programs found
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPrograms.map((program, index) => (
                <motion.div
                  key={program.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
                >
                  <div className="relative">
                    <div className="aspect-video bg-gray-200 flex items-center justify-center">
                      <Play className="w-12 h-12 text-gray-400" />
                    </div>
                    <div className="absolute top-3 right-3">
                      <button className="w-8 h-8 bg-black/20 hover:bg-black/30 rounded-full flex items-center justify-center transition-colors">
                        <Heart className="w-4 h-4 text-white" />
                      </button>
                    </div>
                    <div className="absolute bottom-3 left-3">
                      <span className="bg-black/60 text-white px-2 py-1 rounded text-xs font-medium">
                        {program.level}
                      </span>
                    </div>
                  </div>
                  
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-900 mb-2">{program.title}</h3>
                    <p className="text-sm text-gray-600 mb-3">{program.description}</p>
                    
                    <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{program.duration}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Star className="w-4 h-4 text-yellow-400 fill-current" />
                        <span>{program.rating}</span>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between mb-4">
                      <div className="text-xs text-gray-500">
                        by {program.instructor}
                      </div>
                      <div className="text-xs text-gray-500">
                        {program.completions.toLocaleString()} completions
                      </div>
                    </div>
                    
                    <Button
                      fullWidth
                      icon={Play}
                      iconPosition="left"
                    >
                      Start Program
                    </Button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgramsLibrary;