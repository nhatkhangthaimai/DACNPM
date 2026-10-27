import React from 'react';

interface MatchScoreRingProps {
  score: number;
  size?: number;
  strokeWidth?: number;
  showLabel?: boolean;
  className?: string;
}

export const MatchScoreRing: React.FC<MatchScoreRingProps> = ({
  score,
  size = 110,
  strokeWidth = 9,
  showLabel = true,
  className = '',
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const clampedScore = Math.max(0, Math.min(100, score));
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  // Determine dynamic color based on score
  const getColor = (val: number) => {
    if (val >= 85) return '#C9F16A'; // Lime accent
    if (val >= 70) return '#68DCC5'; // Mint
    if (val >= 50) return '#FFCE7D'; // Gold
    return '#FF876D'; // Coral
  };

  const ringColor = getColor(clampedScore);

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#1E3554"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="opacity-30"
        />
        {/* Animated score indicator */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={ringColor}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="font-heading font-bold text-2xl tracking-tight text-signal-navy dark:text-white">
          {clampedScore}%
        </span>
        {showLabel && (
          <span className="text-[10px] uppercase font-semibold text-signal-slate tracking-wider">
            Match
          </span>
        )}
      </div>
    </div>
  );
};
