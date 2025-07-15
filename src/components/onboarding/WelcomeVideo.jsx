import React from 'react';
import { motion } from 'framer-motion';

const WelcomeVideo = ({ onComplete }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 text-center">
          Welcome to Team Welly! 🎉
        </h2>
        
        <div className="aspect-video bg-gray-200 rounded-lg mb-6 flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
              </svg>
            </div>
            <p className="text-gray-600 text-sm">
              "What is Team Welly?"
            </p>
            <p className="text-gray-500 text-xs mt-1">
              2:30 min introduction video
            </p>
          </div>
        </div>
        
        <div className="space-y-3">
          <button
            onClick={onComplete}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded-lg transition-colors"
          >
            Get Started
          </button>
          <button
            onClick={onComplete}
            className="w-full text-gray-600 hover:text-gray-800 font-medium py-2"
          >
            Skip for now
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default WelcomeVideo;