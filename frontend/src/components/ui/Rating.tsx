'use client';

import { cn } from '@/lib/utils';

interface RatingProps {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  interactive?: boolean;
  onChange?: (n: number) => void;
}

export function Rating({ value, max = 5, size = 'md', interactive = false, onChange }: RatingProps) {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-7 w-7',
  };
  return (
    <div className="flex items-center gap-1" aria-label={`${value.toFixed(1)} out of ${max}`}>
      {Array.from({ length: max }, (_, index) => {
        const score = index + 1;
        const filled = score <= Math.round(value);
        const star = (
          <svg
            className={cn(sizes[size], filled ? 'fill-accent text-accent' : 'fill-none text-slate-300')}
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="1.8"
            aria-hidden="true"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="m12 3.2 2.7 5.47 6.03.88-4.36 4.25 1.03 6-5.4-2.84-5.4 2.84 1.03-6-4.36-4.25 6.03-.88L12 3.2Z" />
          </svg>
        );
        if (!interactive) {
          return <span key={score}>{star}</span>;
        }
        return (
          <button
            key={score}
            type="button"
            onClick={() => onChange?.(score)}
            className="rounded-full p-0.5 focus:outline-none focus:ring-2 focus:ring-primary"
            aria-label={`Set rating to ${score}`}
          >
            {star}
          </button>
        );
      })}
    </div>
  );
}
