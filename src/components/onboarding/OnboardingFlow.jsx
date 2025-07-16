import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../hooks/useAuth';
import Button from '../common/Button';
import { Heart, ArrowRight, Target } from 'lucide-react';

const OnboardingFlow = () => {
  const { actions, isAuthenticated, hasCompletedOnboarding, isLoading } = useAuth();
  const [isProcessing, setIsProcessing] = useState(false);

  const handleStartJourney = async () => {
    setIsProcessing(true);
    
    try {
      console.log('Starting onboarding process...');
      
      // If not authenticated, create a demo user
      if (!isAuthenticated) {
        console.log('Creating demo user...');
        await actions.signUp({
          email: 'demo@teamwelly.com',
          name: 'Demo User',
          plan: 'basic'
        });
      }
      
      // Set demo goals and assessment data
      console.log('Setting goals and assessment data...');
      actions.setSelectedGoals(['Reduce Pain', 'Improve Flexibility']);
      actions.setAssessmentData({
        stressLevel: 6,
        sleepQuality: 7,
        painAreas: ['neck', 'shoulders'],
        movementHabits: 'sedentary'
      });
      
      // Complete onboarding
      console.log('Completing onboarding...');
      actions.completeOnboarding();
      
    } catch (error) {
      console.error('Error during onboarding:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center"
      >
        <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <Heart className="w-8 h-8 text-white" />
        </div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome to Team Welly
        </h1>
        
        <p className="text-gray-600 mb-8">
          Your comprehensive health and wellness companion. Let's get you started on your journey to better health.
        </p>
        
        <div className="space-y-4">
          <Button
            fullWidth
            onClick={handleStartJourney}
            icon={Target}
            iconPosition="left"
            loading={isProcessing || isLoading}
            disabled={isProcessing || isLoading}
          >
            {isProcessing || isLoading ? 'Setting up...' : 'Start Your Wellness Journey'}
          </Button>
          
          <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
            <span>Complete setup in 2 minutes</span>
            <ArrowRight className="w-4 h-4" />
          </div>
        </div>
        
        <div className="mt-8 text-xs text-gray-400">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </div>
        
        {/* Debug info - remove in production */}
        <div className="mt-4 text-xs text-gray-500 bg-gray-50 p-2 rounded">
          Debug: Auth: {isAuthenticated ? 'Yes' : 'No'} | Onboarded: {hasCompletedOnboarding ? 'Yes' : 'No'}
        </div>
      </motion.div>
    </div>
  );
};

export default OnboardingFlow;