'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import { VendorCard } from '@/components/vendors/VendorCard';
import { Button } from '@/components/ui/Button';
import { EmptyState } from '@/components/ui/EmptyState';
import { Input } from '@/components/ui/Input';
import { LoadingState } from '@/components/ui/LoadingState';
import { FOOD_CATEGORIES } from '@/lib/constants';
import { getVendors } from '@/lib/api';
import type { Vendor } from '@/lib/types';
import { getCategoryEmoji } from '@/lib/utils';

export default function HomePage() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [openVendors, setOpenVendors] = useState<Vendor[]>([]);
  const [popularVendors, setPopularVendors] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    async function load() {
      try {
        setLoading(true);
        const [open, popular] = await Promise.all([
          getVendors({ open_now: true, limit: 6 }),
          getVendors({ limit: 6 }),
        ]);
        if (!alive) {
          return;
        }
        setOpenVendors(open.vendors);
        setPopularVendors(popular.vendors);
        setError(null);
      } catch (requestError) {
        if (alive) {
          setError(requestError instanceof Error ? requestError.message : 'Unable to load vendors');
        }
      } finally {
        if (alive) {
          setLoading(false);
        }
      }
    }
    load();
    return () => {
      alive = false;
    };
  }, []);

  function submitSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const params = new URLSearchParams();
    if (query.trim()) {
      params.set('q', query.trim());
    }
    router.push(`/vendors${params.toString() ? `?${params.toString()}` : ''}`);
  }

  return (
    <div>
      <section className="bg-[radial-gradient(circle_at_top_left,#F7C94833,transparent_32%),linear-gradient(135deg,#FFFAF5,#FFF)]">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-16 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:px-8 lg:py-20">
          <div className="flex flex-col justify-center">
            <h1 className="max-w-3xl text-4xl font-extrabold leading-tight text-secondary sm:text-5xl lg:text-6xl">
              Discover Bangalore&apos;s Best Street Food
            </h1>
            <p className="mt-5 max-w-2xl text-lg text-slate-600">
              Real vendors. Real timings. Real hygiene ratings.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/vendors" className="rounded-full bg-primary px-5 py-3 font-bold text-white transition hover:bg-primary/90">
                Explore Vendors
              </Link>
              <Link href="/map" className="rounded-full border border-primary px-5 py-3 font-bold text-primary transition hover:bg-primary/10">
                View Map
              </Link>
            </div>
            <form onSubmit={submitSearch} className="mt-8 flex max-w-xl flex-col gap-3 rounded-2xl bg-white p-2 shadow-sm sm:flex-row">
              <Input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search by dish, area, or vendor"
                className="border-transparent"
              />
              <Button type="submit" className="shrink-0">
                Search
              </Button>
            </form>
          </div>
          <div className="grid content-center gap-4 sm:grid-cols-2">
            {['Dosa at dawn', 'Chaat after work', 'Tea between meetings', 'Dessert after dinner'].map((label, index) => (
              <div key={label} className={`rounded-2xl bg-white p-6 shadow-sm ${index % 2 === 1 ? 'sm:translate-y-8' : ''}`}>
                <div className="text-4xl">{['🫓', '🍛', '☕', '🍮'][index]}</div>
                <p className="mt-4 text-lg font-bold text-secondary">{label}</p>
                <p className="mt-2 text-sm text-slate-600">Fresh picks across Bangalore neighborhoods.</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex gap-3 overflow-x-auto pb-3">
          {FOOD_CATEGORIES.map((category) => (
            <Link
              key={category}
              href={`/vendors?category=${encodeURIComponent(category)}`}
              className="shrink-0 rounded-full bg-white px-4 py-2 text-sm font-bold text-secondary shadow-sm transition hover:bg-orange-100"
            >
              {getCategoryEmoji(category)} {category}
            </Link>
          ))}
        </div>
      </section>

      <section className="bg-white">
        <div className="mx-auto grid max-w-7xl gap-4 px-4 py-8 sm:grid-cols-2 sm:px-6 lg:grid-cols-4 lg:px-8">
          {['Nearby Only', 'Live Timings', 'Hygiene Ratings', 'Map Directions'].map((item, index) => (
            <div key={item} className="flex items-center gap-3">
              <span className="flex h-11 w-11 items-center justify-center rounded-full bg-orange-100 text-xl">
                {['📍', '⏱️', '🧼', '🗺️'][index]}
              </span>
              <span className="font-bold text-secondary">{item}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        {loading ? (
          <LoadingState />
        ) : error ? (
          <EmptyState title="Could not load vendors" description={error} />
        ) : (
          <div className="space-y-12">
            <div>
              <div className="mb-5 flex items-center justify-between gap-4">
                <h2 className="text-2xl font-extrabold text-secondary">Open Now</h2>
                <Link href="/vendors?open_now=true" className="text-sm font-bold text-primary">
                  See all open vendors →
                </Link>
              </div>
              <div className="flex gap-4 overflow-x-auto pb-3">
                {openVendors.map((vendor) => (
                  <div key={vendor.id} className="w-80 shrink-0">
                    <VendorCard vendor={vendor} />
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h2 className="mb-5 text-2xl font-extrabold text-secondary">Popular Near You</h2>
              <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
                {popularVendors.map((vendor) => (
                  <VendorCard key={vendor.id} vendor={vendor} />
                ))}
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
