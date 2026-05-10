import type { HTMLAttributes, ReactNode } from 'react';

import { cn } from '@/lib/utils';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function Card({ children, className, ...props }: CardProps) {
  return (
    <div
      className={cn('rounded-2xl border border-orange-100 bg-white p-5 shadow-sm transition hover:shadow-md', className)}
      {...props}
    >
      {children}
    </div>
  );
}
