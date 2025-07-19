import React from 'react';

const ProgressRing = ({ 
  progress = 0, 
  size = 120, 
  strokeWidth = 8, 
  color = '#059669',
  backgroundColor = '#e5e7eb',
  showPercentage = true,
  label = '',
  animated = true
}) => {
  const center = size / 2;
  const radius = center - strokeWidth / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center">
      <svg
        width={size}
        height={size}
        className={`transform -rotate-90 ${animated ? 'transition-all duration-500' : ''}`}
      >
        {/* Background circle */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={backgroundColor}
          strokeWidth={strokeWidth}
        />
        
        {/* Progress circle */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className={animated ? 'transition-all duration-500 ease-out' : ''}
        />
      </svg>
      
      {/* Content in center */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        {showPercentage && (
          <span className="text-lg font-bold text-gray-900">
            {Math.round(progress)}%
          </span>
        )}
        {label && (
          <span className="text-xs text-gray-500 mt-1 text-center">
            {label}
          </span>
        )}
      </div>
    </div>
  );
};

export default ProgressRing;