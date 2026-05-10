'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';

import { cn } from '@/lib/utils';

const links = [
  { href: '/', label: 'Home' },
  { href: '/vendors', label: 'Vendors' },
  { href: '/map', label: 'Map' },
];

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-orange-100 bg-background/95 backdrop-blur">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/" className="text-lg font-extrabold text-secondary" onClick={() => setOpen(false)}>
          🍜 Street Food Finder
        </Link>
        <div className="hidden items-center gap-2 md:flex">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                'rounded-full px-4 py-2 text-sm font-semibold transition',
                pathname === link.href ? 'bg-primary text-white' : 'text-slate-700 hover:bg-orange-100',
              )}
            >
              {link.label}
            </Link>
          ))}
        </div>
        <button
          type="button"
          className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-orange-100 bg-white text-xl md:hidden"
          onClick={() => setOpen((value) => !value)}
          aria-label="Open navigation menu"
        >
          ☰
        </button>
      </nav>
      {open ? (
        <div className="border-t border-orange-100 bg-white px-4 py-3 shadow-md md:hidden">
          <div className="mx-auto flex max-w-7xl flex-col gap-2">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className={cn(
                  'rounded-2xl px-4 py-3 text-sm font-semibold',
                  pathname === link.href ? 'bg-primary text-white' : 'bg-background text-secondary',
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      ) : null}
    </header>
  );
}
