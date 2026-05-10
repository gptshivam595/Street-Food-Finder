import type { Metadata } from 'next';

import { Footer } from '@/components/layout/Footer';
import { Navbar } from '@/components/layout/Navbar';

import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'Street Food Finder',
  description: 'Discover Bangalore street food vendors with timings, hygiene ratings, menus, and maps.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="min-h-screen text-secondary antialiased">
        <Navbar />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
