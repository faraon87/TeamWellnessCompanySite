import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Heart, 
  Shield, 
  Zap, 
  Users, 
  MessageCircle,
  Play,
  Star,
  Award,
  Clock,
  User,
  Settings,
  LogOut,
  X,
  Send,
  Sparkles,
  TrendingUp,
  Calendar,
  CreditCard,
  CheckCircle,
  Lock,
  Mail,
  Eye,
  EyeOff
} from 'lucide-react';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Enhanced Team Welly App with Modern UI/UX
const TeamWellyApp = () => {
  const [currentView, setCurrentView] = useState('welcome');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [programs, setPrograms] = useState([]);
  const [userProgress, setUserProgress] = useState({});
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  const [showPassword, setShowPassword] = useState(false);
  const [authForm, setAuthForm] = useState({
    email: '',
    password: '',
    name: '',
    plan: 'basic'
  });

  useEffect(() => {
    checkAuthentication();
    if (isAuthenticated) {
      loadUserData();
    }
  }, [isAuthenticated]);

  const checkAuthentication = async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const response = await api.get('/api/auth/me');
        setUser(response.data);
        setIsAuthenticated(true);
        setCurrentView('dashboard');
      } catch (error) {
        console.error('Authentication check failed:', error);
        localStorage.removeItem('access_token');
      }
    }
    setLoading(false);
  };

  const loadUserData = async () => {
    try {
      const [programsRes, analyticsRes] = await Promise.all([
        api.get('/api/programs/'),
        api.get('/api/analytics/progress').catch(() => ({ data: {} }))
      ]);
      
      setPrograms(programsRes.data);
      setUserProgress(analyticsRes.data);
    } catch (error) {
      console.error('Failed to load user data:', error);
    }
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const endpoint = authMode === 'login' ? '/api/auth/login' : '/api/auth/signup';
      const response = await api.post(endpoint, authForm);
      
      localStorage.setItem('access_token', response.data.access_token);
      setUser(response.data.user);
      setIsAuthenticated(true);
      setCurrentView('dashboard');
      setShowAuth(false);
      showNotification('Welcome to Team Welly!', 'success');
    } catch (error) {
      console.error('Authentication failed:', error);
      showNotification('Authentication failed. Please try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleAuth = async () => {
    try {
      showNotification('Google OAuth integration coming soon!', 'info');
      // window.location.href = `${API_BASE_URL}/api/auth/google/login`;
    } catch (error) {
      console.error('Google auth failed:', error);
    }
  };

  const handleAppleAuth = async () => {
    try {
      showNotification('Apple Sign In integration coming soon!', 'info');
      // window.location.href = `${API_BASE_URL}/api/auth/apple/login`;
    } catch (error) {
      console.error('Apple auth failed:', error);
    }
  };

  const handlePayment = async (packageType) => {
    try {
      showNotification(`${packageType} payment integration coming soon!`, 'info');
      // const response = await api.post('/api/payments/create-checkout-session', {
      //   package_type: packageType
      // });
      // window.location.href = response.data.checkout_url;
    } catch (error) {
      console.error('Payment failed:', error);
      showNotification('Payment processing failed. Please try again.', 'error');
    }
  };

  const handleProgramStart = async (programId) => {
    try {
      await api.post(`/api/programs/${programId}/start`);
      showNotification('Program started successfully!', 'success');
      loadUserData();
    } catch (error) {
      console.error('Failed to start program:', error);
      showNotification('Failed to start program', 'error');
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMessage = chatInput.trim();
    setChatInput('');
    setChatLoading(true);

    setChatMessages(prev => [...prev, { 
      type: 'user', 
      message: userMessage, 
      timestamp: new Date() 
    }]);

    try {
      const response = await api.post('/api/ai/chat', {
        message: userMessage,
        user_id: user.id,
        session_id: `session-${Date.now()}`
      });

      setChatMessages(prev => [...prev, { 
        type: 'ai', 
        message: response.data.response, 
        timestamp: new Date(),
        insights: response.data.user_insights,
        recommendations: response.data.recommendations
      }]);

    } catch (error) {
      console.error('Chat failed:', error);
      setChatMessages(prev => [...prev, { 
        type: 'ai', 
        message: 'I\'m having trouble responding right now. Please try again!', 
        timestamp: new Date()
      }]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    setUser(null);
    setCurrentView('welcome');
    showNotification('Logged out successfully', 'success');
  };

  const showNotification = (message, type = 'info') => {
    const notification = document.createElement('div');
    const colors = {
      success: 'bg-green-500',
      error: 'bg-red-500',
      info: 'bg-blue-500'
    };
    
    notification.className = `fixed top-6 right-6 ${colors[type]} text-white px-6 py-3 rounded-xl shadow-lg z-50 transform transition-all duration-300`;
    notification.textContent = message;
    notification.style.transform = 'translateX(100%)';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
      notification.style.transform = 'translateX(100%)';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600 font-medium">Loading Team Welly...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-xl p-8 text-center"
          >
            <div className="w-20 h-20 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <Heart className="w-10 h-10 text-white" />
            </div>
            
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Team Welly</h1>
            <p className="text-gray-600 mb-8">Your AI-powered wellness companion</p>
            
            <div className="space-y-3">
              <button
                onClick={() => setShowAuth(true)}
                className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-emerald-600 hover:to-teal-700 transition-all duration-200 transform hover:scale-105"
              >
                <Sparkles className="w-5 h-5 inline mr-2" />
                Start Your Journey
              </button>
              
              <button
                onClick={handleGoogleAuth}
                className="w-full bg-white text-gray-700 py-3 px-6 rounded-xl font-semibold border-2 border-gray-200 hover:border-gray-300 transition-all duration-200 flex items-center justify-center gap-2"
              >
                <div className="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs font-bold">G</span>
                </div>
                Continue with Google
              </button>
              
              <button
                onClick={handleAppleAuth}
                className="w-full bg-black text-white py-3 px-6 rounded-xl font-semibold hover:bg-gray-800 transition-all duration-200 flex items-center justify-center gap-2"
              >
                <div className="w-5 h-5 bg-white rounded-full flex items-center justify-center">
                  <span className="text-black text-xs font-bold">🍎</span>
                </div>
                Continue with Apple
              </button>
            </div>
            
            <div className="mt-8 p-4 bg-gray-50 rounded-xl">
              <h3 className="font-semibold text-gray-900 mb-3">What's New:</h3>
              <ul className="text-sm text-gray-600 space-y-2">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  AI-powered wellness coaching
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Personalized program recommendations
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Real-time progress tracking
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Secure payment integration
                </li>
              </ul>
            </div>
          </motion.div>
        </div>
        
        {/* Auth Modal */}
        <AnimatePresence>
          {showAuth && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md"
              >
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">
                    {authMode === 'login' ? 'Welcome Back' : 'Join Team Welly'}
                  </h2>
                  <button
                    onClick={() => setShowAuth(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-6 h-6" />
                  </button>
                </div>
                
                <form onSubmit={handleAuth} className="space-y-4">
                  {authMode === 'signup' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Full Name
                      </label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                        <input
                          type="text"
                          value={authForm.name}
                          onChange={(e) => setAuthForm({...authForm, name: e.target.value})}
                          className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                          placeholder="Enter your name"
                          required
                        />
                      </div>
                    </div>
                  )}
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                      <input
                        type="email"
                        value={authForm.email}
                        onChange={(e) => setAuthForm({...authForm, email: e.target.value})}
                        className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                        placeholder="Enter your email"
                        required
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                      <input
                        type={showPassword ? "text" : "password"}
                        value={authForm.password}
                        onChange={(e) => setAuthForm({...authForm, password: e.target.value})}
                        className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                        placeholder="Enter your password"
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                      </button>
                    </div>
                  </div>
                  
                  {authMode === 'signup' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Plan
                      </label>
                      <select
                        value={authForm.plan}
                        onChange={(e) => setAuthForm({...authForm, plan: e.target.value})}
                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                      >
                        <option value="basic">Basic Plan</option>
                        <option value="plus">Plus Plan</option>
                        <option value="premium">Premium Plan</option>
                      </select>
                    </div>
                  )}
                  
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-emerald-600 hover:to-teal-700 transition-all duration-200 disabled:opacity-50"
                  >
                    {loading ? 'Processing...' : authMode === 'login' ? 'Sign In' : 'Create Account'}
                  </button>
                </form>
                
                <div className="mt-6 text-center">
                  <button
                    onClick={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')}
                    className="text-emerald-600 hover:text-emerald-700 font-medium"
                  >
                    {authMode === 'login' ? 'Need an account? Sign up' : 'Already have an account? Sign in'}
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-full flex items-center justify-center">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Team Welly</h1>
                <p className="text-sm text-gray-500">Welcome back, {user?.name}!</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-4">
                <div className="bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-sm font-medium">
                  <Award className="w-4 h-4 inline mr-1" />
                  {userProgress.current_metrics?.welly_points || 0} pts
                </div>
                <div className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">
                  <TrendingUp className="w-4 h-4 inline mr-1" />
                  {userProgress.current_metrics?.current_streak || 0} days
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setCurrentView('settings')}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                >
                  <Settings className="w-5 h-5" />
                </button>
                <button
                  onClick={handleLogout}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Dashboard */}
            <div className="lg:col-span-2 space-y-6">
              {/* Welcome Card */}
              <div className="bg-gradient-to-r from-emerald-500 to-teal-600 rounded-2xl p-6 text-white">
                <h2 className="text-2xl font-bold mb-2">Good morning! 🌅</h2>
                <p className="text-emerald-100 mb-4">Ready to make today amazing?</p>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => setCurrentView('programs')}
                    className="bg-white text-emerald-600 px-4 py-2 rounded-xl font-medium hover:bg-emerald-50 transition-colors"
                  >
                    <Play className="w-4 h-4 inline mr-2" />
                    Start Program
                  </button>
                  <button
                    onClick={() => setShowChat(true)}
                    className="bg-emerald-600 text-white px-4 py-2 rounded-xl font-medium hover:bg-emerald-700 transition-colors"
                  >
                    <MessageCircle className="w-4 h-4 inline mr-2" />
                    Chat with AI
                  </button>
                </div>
              </div>

              {/* Programs Grid */}
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">Featured Programs</h2>
                  <button
                    onClick={() => setCurrentView('programs')}
                    className="text-emerald-600 hover:text-emerald-700 font-medium"
                  >
                    View All
                  </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {programs.slice(0, 4).map((program) => (
                    <div
                      key={program.id}
                      className="bg-gray-50 rounded-xl p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="font-semibold text-gray-900">{program.title}</h3>
                        <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded">
                          {program.duration} min
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{program.description}</p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-1">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                          ))}
                          <span className="text-sm text-gray-500 ml-2">4.9</span>
                        </div>
                        <button
                          onClick={() => handleProgramStart(program.id)}
                          className="bg-emerald-500 text-white px-3 py-1 rounded-lg text-sm font-medium hover:bg-emerald-600 transition-colors"
                        >
                          Start
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Progress Card */}
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Today's Progress</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center">
                        <Heart className="w-5 h-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Wellness Score</p>
                        <p className="text-sm text-gray-500">Daily target: 80%</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-emerald-600">75%</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <Calendar className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Sessions</p>
                        <p className="text-sm text-gray-500">This week</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-blue-600">12</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Membership Card */}
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Membership</h2>
                <div className="bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl p-4 text-white mb-4">
                  <p className="text-sm text-purple-100">Current Plan</p>
                  <p className="text-xl font-bold">{user?.plan || 'Basic'} Plan</p>
                </div>
                <button
                  onClick={() => handlePayment('upgrade')}
                  className="w-full bg-gradient-to-r from-purple-500 to-pink-600 text-white py-2 px-4 rounded-xl font-medium hover:from-purple-600 hover:to-pink-700 transition-all duration-200"
                >
                  <CreditCard className="w-4 h-4 inline mr-2" />
                  Upgrade Plan
                </button>
              </div>
            </div>
          </div>
        )}

        {currentView === 'settings' && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Settings</h2>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Profile</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                      <input
                        type="text"
                        value={user?.name || ''}
                        readOnly
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                      <input
                        type="email"
                        value={user?.email || ''}
                        readOnly
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
                      />
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Integrations</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-gray-900">Google OAuth</span>
                      <span className="text-sm text-orange-600">Coming Soon</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-gray-900">Apple Sign In</span>
                      <span className="text-sm text-orange-600">Coming Soon</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-gray-900">Stripe Payments</span>
                      <span className="text-sm text-orange-600">Coming Soon</span>
                    </div>
                  </div>
                </div>
                
                <button
                  onClick={() => setCurrentView('dashboard')}
                  className="w-full bg-emerald-500 text-white py-3 px-6 rounded-xl font-semibold hover:bg-emerald-600 transition-colors"
                >
                  Back to Dashboard
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* AI Chat Button */}
      <button
        onClick={() => setShowChat(true)}
        className="fixed bottom-6 right-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-full shadow-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 z-40"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Enhanced AI Chat Modal */}
      <AnimatePresence>
        {showChat && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="fixed bottom-6 right-6 w-96 h-96 bg-white rounded-2xl shadow-xl border border-gray-200 flex flex-col z-50"
          >
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Welly AI</h3>
                  <p className="text-xs text-gray-500">Your wellness coach</p>
                </div>
              </div>
              <button
                onClick={() => setShowChat(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {chatMessages.length === 0 && (
                <div className="text-center py-8">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                  <p className="text-gray-600">Hi! I'm Welly, your AI wellness coach. How can I help you today?</p>
                </div>
              )}
              
              {chatMessages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs px-4 py-2 rounded-2xl ${
                    msg.type === 'user'
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    <p className="text-sm">{msg.message}</p>
                    {msg.recommendations && (
                      <div className="mt-2 p-2 bg-blue-50 rounded-lg">
                        <p className="text-xs font-medium text-blue-700 mb-1">Recommendations:</p>
                        <ul className="text-xs text-blue-600 space-y-1">
                          {msg.recommendations.map((rec, i) => (
                            <li key={i}>• {rec}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {chatLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-2xl px-4 py-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <form onSubmit={handleChatSubmit} className="p-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask Welly anything..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                  disabled={chatLoading}
                />
                <button
                  type="submit"
                  disabled={chatLoading || !chatInput.trim()}
                  className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-2 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-2 z-30">
        <div className="flex justify-around">
          {[
            { key: 'dashboard', icon: Heart, label: 'Dashboard' },
            { key: 'programs', icon: Play, label: 'Programs' },
            { key: 'coaching', icon: Users, label: 'Coaching' },
            { key: 'analytics', icon: TrendingUp, label: 'Analytics' },
            { key: 'settings', icon: Settings, label: 'Settings' }
          ].map(({ key, icon: Icon, label }) => (
            <button
              key={key}
              onClick={() => setCurrentView(key)}
              className={`flex flex-col items-center py-2 px-3 rounded-lg transition-colors ${
                currentView === key
                  ? 'text-emerald-600 bg-emerald-50'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-xs mt-1">{label}</span>
            </button>
          ))}
        </div>
      </nav>
    </div>
  );
};

export default TeamWellyApp;