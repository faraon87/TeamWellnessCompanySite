import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './contexts/AppContext';
import { AuthProvider } from './contexts/AuthContext';
import OnboardingFlow from './components/onboarding/OnboardingFlow';
import Dashboard from './components/dashboard/Dashboard';
import ProgramsLibrary from './components/programs/ProgramsLibrary';
import LiveCoaching from './components/coaching/LiveCoaching';
import Challenges from './components/challenges/Challenges';
import Settings from './components/settings/Settings';
import AdminPortal from './components/admin/AdminPortal';
import Navigation from './components/common/Navigation';
import { useAuth } from './hooks/useAuth';
import PWAInstallPrompt from './components/common/PWAInstallPrompt';
import LoadingSpinner from './components/common/LoadingSpinner';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Register service worker for PWA
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
          console.log('SW registered: ', registration);
        })
        .catch((registrationError) => {
          console.log('SW registration failed: ', registrationError);
        });
    }

    // Simulate app initialization
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, []);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <AuthProvider>
      <AppProvider>
        <Router>
          <div className="app">
            <PWAInstallPrompt />
            <AppContent />
          </div>
        </Router>
      </AppProvider>
    </AuthProvider>
  );
}

function AppContent() {
  const { user, isAuthenticated, hasCompletedOnboarding } = useAuth();

  if (!isAuthenticated) {
    return <OnboardingFlow />;
  }

  if (!hasCompletedOnboarding) {
    return <OnboardingFlow />;
  }

  return (
    <div className="app-layout">
      <Navigation />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/programs" element={<ProgramsLibrary />} />
          <Route path="/coaching" element={<LiveCoaching />} />
          <Route path="/challenges" element={<Challenges />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/admin" element={<AdminPortal />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;