import type { HTMLAttributes, ReactNode } from 'react';

import { cn } from '@/lib/utils';

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  children: ReactNode;
  tone?: 'neutral' | 'success' | 'danger' | 'accent' | 'primary';
}

export function Badge({ children, className, tone = 'neutral', ...props }: BadgeProps) {
  const tones = {
    neutral: 'bg-slate-100 text-slate-700',
    success: 'bg-green-100 text-green-700',
    danger: 'bg-red-100 text-red-700',
    accent: 'bg-yellow-100 text-yellow-800',
    primary: 'bg-orange-100 text-primary',
  };
  return (
    <span className={cn('inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold', tones[tone], className)} {...props}>
      {children}
    </span>
  );
}
