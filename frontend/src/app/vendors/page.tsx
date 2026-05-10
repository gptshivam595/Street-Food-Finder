'use client';

import { Suspense, useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';

import { EmptyState } from '@/components/ui/EmptyState';
import { LoadingState } from '@/components/ui/LoadingState';
import { Button } from '@/components/ui/Button';
import { VendorCard } from '@/components/vendors/VendorCard';
import { VendorFilters } from '@/components/vendors/VendorFilters';
import { getVendors } from '@/lib/api';
import type { Vendor } from '@/lib/types';

const PAGE_SIZE = 12;

function VendorsContent() {
  const searchParams = useSearchParams();
  const [search, setSearch] = useState(searchParams.get('q') ?? '');
  const [category, setCategory] = useState(searchParams.get('category') ?? '');
  const [openNow, setOpenNow] = useState(searchParams.get('open_now') === 'true');
  const [sort, setSort] = useState<'Rating' | 'Distance'>('Rating');
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [loadingLocation, setLoadingLocation] = useState(false);
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadVendors = useCallback(
    async (nextOffset: number, append: boolean) => {
      try {
        append ? setLoadingMore(true) : setLoading(true);
        const response = await getVendors({
          q: search || undefined,
          category: category || undefined,
          open_now: openNow || undefined,
          lat: location?.lat,
          lng: location?.lng,
          limit: PAGE_SIZE,
          offset: nextOffset,
        });
        const sorted = [...response.vendors].sort((a, b) => {
          if (sort === 'Distance' && a.distance_km !== null && b.distance_km !== null) {
            return a.distance_km - b.distance_km;
          }
          return b.average_rating - a.average_rating;
        });
        setVendors((current) => (append ? [...current, ...sorted] : sorted));
        setTotal(response.total);
        setOffset(nextOffset);
        setError(null);
      } catch (requestError) {
        setError(requestError instanceof Error ? requestError.message : 'Unable to load vendors');
      } finally {
        setLoading(false);
        setLoadingMore(false);
      }
    },
    [category, location?.lat, location?.lng, openNow, search, sort],
  );

  useEffect(() => {
    loadVendors(0, false);
  }, [loadVendors]);

  const requestLocation = useCallback(() => {
    if (!navigator.geolocation) {
      setError('Location is not available in this browser');
      return;
    }
    setLoadingLocation(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({ lat: position.coords.latitude, lng: position.coords.longitude });
        setSort('Distance');
        setLoadingLocation(false);
      },
      () => {
        setError('Could not access your location');
        setLoadingLocation(false);
      },
      { enableHighAccuracy: true, timeout: 8000 },
    );
  }, []);

  const hasMore = useMemo(() => vendors.length < total, [total, vendors.length]);

  return (
    <div className="mx-auto grid max-w-7xl gap-6 px-4 py-8 sm:px-6 lg:grid-cols-[320px_1fr] lg:px-8">
      <VendorFilters
        search={search}
        category={category}
        openNow={openNow}
        sort={sort}
        hasLocation={location !== null}
        loadingLocation={loadingLocation}
        onSearchChange={setSearch}
        onCategoryChange={setCategory}
        onOpenNowChange={setOpenNow}
        onSortChange={setSort}
        onUseLocation={requestLocation}
      />
      <section>
        <div className="mb-5 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <h1 className="text-3xl font-extrabold text-secondary">Vendors</h1>
          <p className="text-sm font-semibold text-slate-600">Showing {total} vendors</p>
        </div>
        {loading ? (
          <LoadingState />
        ) : error ? (
          <EmptyState title="Could not load vendors" description={error} />
        ) : vendors.length === 0 ? (
          <EmptyState title="No vendors found" description="Try a different search, category, or timing filter." />
        ) : (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {vendors.map((vendor) => (
                <VendorCard key={vendor.id} vendor={vendor} showDistance={location !== null} />
              ))}
            </div>
            {hasMore ? (
              <div className="mt-8 text-center">
                <Button type="button" onClick={() => loadVendors(offset + PAGE_SIZE, true)} disabled={loadingMore}>
                  {loadingMore ? 'Loading...' : 'Load More'}
                </Button>
              </div>
            ) : null}
          </>
        )}
      </section>
    </div>
  );
}

export default function VendorsPage() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-7xl px-4 py-8"><LoadingState /></div>}>
      <VendorsContent />
    </Suspense>
  );
}
