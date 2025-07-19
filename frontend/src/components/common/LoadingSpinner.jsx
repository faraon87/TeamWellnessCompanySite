import React from 'react';

const LoadingSpinner = ({ size = 'medium', text = 'Loading...' }) => {
  const sizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12'
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-emerald-50">
      <div className="relative">
        <div className={`${sizeClasses[size]} border-4 border-green-200 border-t-green-600 rounded-full animate-spin`}></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-2 h-2 bg-green-600 rounded-full animate-ping"></div>
        </div>
      </div>
      <p className="mt-4 text-gray-600 font-medium">{text}</p>
      <div className="mt-2 text-sm text-gray-500">Team Welly</div>
    </div>
  );
};

export default LoadingSpinner;