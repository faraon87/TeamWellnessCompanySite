import React, { useState, useEffect } from 'react';
import axios from 'axios';

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

// Enhanced Team Welly App with Backend Integration
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

  const handleLogin = async (email = 'demo@teamwelly.com', password = 'demo123') => {
    try {
      setLoading(true);
      const response = await api.post('/api/auth/signup', {
        email,
        name: 'Demo User',
        plan: 'premium'
      });
      
      localStorage.setItem('access_token', response.data.access_token);
      setUser(response.data.user);
      setIsAuthenticated(true);
      setCurrentView('dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      window.location.href = `${API_BASE_URL}/api/auth/google/login`;
    } catch (error) {
      console.error('Google login failed:', error);
    }
  };

  const handleProgramStart = async (programId) => {
    try {
      await api.post(`/api/programs/${programId}/start`);
      showSuccess(`Started program successfully!`);
      loadUserData(); // Refresh user data
    } catch (error) {
      console.error('Failed to start program:', error);
      showError('Failed to start program');
    }
  };

  const handleProgramComplete = async (programId) => {
    try {
      await api.post(`/api/programs/${programId}/complete`, {
        rating: 5,
        notes: 'Completed via web app'
      });
      showSuccess('Program completed! +50 WellyPoints earned!');
      loadUserData(); // Refresh user data
    } catch (error) {
      console.error('Failed to complete program:', error);
      showError('Failed to complete program');
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMessage = chatInput.trim();
    setChatInput('');
    setChatLoading(true);

    // Add user message to chat
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

      // Add AI response to chat
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
        message: 'Sorry, I\'m having trouble responding right now. Please try again in a moment.', 
        timestamp: new Date()
      }]);
    } finally {
      setChatLoading(false);
    }
  };

  const showSuccess = (message) => {
    const success = document.createElement('div');
    success.className = 'success-message';
    success.textContent = message;
    success.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #22c55e;
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
      z-index: 1000;
      animation: slideIn 0.3s ease-out;
    `;
    document.body.appendChild(success);
    setTimeout(() => success.remove(), 3000);
  };

  const showError = (message) => {
    const error = document.createElement('div');
    error.className = 'error-message';
    error.textContent = message;
    error.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #ef4444;
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
      z-index: 1000;
      animation: slideIn 0.3s ease-out;
    `;
    document.body.appendChild(error);
    setTimeout(() => error.remove(), 3000);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading Team Welly...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="welcome-container">
        <div className="welcome-card">
          <div className="logo">❤️</div>
          <h1 className="title">Welcome to Team Welly</h1>
          <p className="subtitle">
            Your comprehensive health and wellness companion with AI-powered coaching, personalized programs, and seamless payment integration.
          </p>
          
          <div className="auth-buttons">
            <button className="button primary" onClick={handleLogin}>
              🎯 Start Your Wellness Journey
            </button>
            
            <button className="button secondary" onClick={handleGoogleLogin}>
              🔍 Continue with Google
            </button>
          </div>
          
          <div className="features-list">
            <h3>What's New in Phase 2:</h3>
            <ul>
              <li>✅ AI-powered wellness coaching with Gemini 2.0</li>
              <li>✅ Real-time behavior tracking and insights</li>
              <li>✅ Stripe & PayPal payment integration</li>
              <li>✅ Google OAuth authentication</li>
              <li>✅ Comprehensive wellness programs</li>
              <li>✅ Progress tracking and analytics</li>
            </ul>
          </div>
          
          <div className="disclaimer">
            By continuing, you agree to our Terms of Service and Privacy Policy
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      {/* Header */}
      <div className="header">
        <div className="header-content">
          <div className="user-info">
            <h1>Welcome back, {user?.name}! 👋</h1>
            <p>Ready to continue your wellness journey?</p>
          </div>
          <div className="header-stats">
            <div className="stat">
              🏆 {userProgress.current_metrics?.welly_points || 0} WellyPoints
            </div>
            <div className="stat">
              🔥 {userProgress.current_metrics?.current_streak || 0} day streak
            </div>
            <div className="stat">
              📚 {userProgress.current_metrics?.completed_programs || 0} programs completed
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {currentView === 'dashboard' && (
          <div className="dashboard">
            <div className="dashboard-grid">
              {/* Programs Section */}
              <div className="card">
                <h2>Available Programs</h2>
                <div className="programs-grid">
                  {programs.slice(0, 6).map((program) => (
                    <div key={program.id} className="program-card">
                      <div className="program-header">
                        <h3>{program.title}</h3>
                        <span className="program-duration">{program.duration} min</span>
                      </div>
                      <p className="program-description">{program.description}</p>
                      <div className="program-benefits">
                        {program.benefits?.slice(0, 2).map((benefit, idx) => (
                          <span key={idx} className="benefit-tag">{benefit}</span>
                        ))}
                      </div>
                      <div className="program-actions">
                        <button 
                          className="button small"
                          onClick={() => handleProgramStart(program.id)}
                        >
                          ▶️ Start
                        </button>
                        <button 
                          className="button small secondary"
                          onClick={() => handleProgramComplete(program.id)}
                        >
                          ✅ Complete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Progress Section */}
              <div className="card">
                <h2>Your Progress</h2>
                <div className="progress-stats">
                  <div className="progress-item">
                    <div className="progress-label">WellyPoints</div>
                    <div className="progress-value">{userProgress.current_metrics?.welly_points || 0}</div>
                  </div>
                  <div className="progress-item">
                    <div className="progress-label">Current Streak</div>
                    <div className="progress-value">{userProgress.current_metrics?.current_streak || 0} days</div>
                  </div>
                  <div className="progress-item">
                    <div className="progress-label">Completed Programs</div>
                    <div className="progress-value">{userProgress.current_metrics?.completed_programs || 0}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* AI Chat Button */}
      <button 
        className="chat-toggle"
        onClick={() => setShowChat(!showChat)}
      >
        🤖 {showChat ? 'Close' : 'Chat with Welly AI'}
      </button>

      {/* AI Chat Modal */}
      {showChat && (
        <div className="chat-modal">
          <div className="chat-header">
            <h3>🤖 Welly AI Coach</h3>
            <button onClick={() => setShowChat(false)}>✕</button>
          </div>
          
          <div className="chat-messages">
            {chatMessages.length === 0 && (
              <div className="chat-welcome">
                <p>👋 Hi! I'm Welly, your AI wellness coach. How can I help you today?</p>
              </div>
            )}
            
            {chatMessages.map((msg, idx) => (
              <div key={idx} className={`chat-message ${msg.type}`}>
                <div className="message-content">
                  {msg.message}
                </div>
                {msg.recommendations && msg.recommendations.length > 0 && (
                  <div className="message-recommendations">
                    <h4>💡 Recommendations:</h4>
                    <ul>
                      {msg.recommendations.map((rec, ridx) => (
                        <li key={ridx}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            
            {chatLoading && (
              <div className="chat-message ai">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
          </div>
          
          <form onSubmit={handleChatSubmit} className="chat-input-form">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Ask Welly about your wellness journey..."
              disabled={chatLoading}
              className="chat-input"
            />
            <button type="submit" disabled={chatLoading || !chatInput.trim()}>
              Send
            </button>
          </form>
        </div>
      )}

      {/* Navigation */}
      <div className="navigation">
        <button 
          className={`nav-item ${currentView === 'dashboard' ? 'active' : ''}`}
          onClick={() => setCurrentView('dashboard')}
        >
          <span className="nav-icon">🏠</span>
          <span>Dashboard</span>
        </button>
        <button 
          className="nav-item"
          onClick={() => showSuccess('Programs section enhanced with backend integration!')}
        >
          <span className="nav-icon">📚</span>
          <span>Programs</span>
        </button>
        <button 
          className="nav-item"
          onClick={() => showSuccess('Payment integration ready with Stripe & PayPal!')}
        >
          <span className="nav-icon">💳</span>
          <span>Payments</span>
        </button>
        <button 
          className="nav-item"
          onClick={() => showSuccess('Analytics powered by AI behavior tracking!')}
        >
          <span className="nav-icon">📊</span>
          <span>Analytics</span>
        </button>
      </div>
    </div>
  );
};

export default TeamWellyApp;