'use client';

import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';

import { EmptyState } from '@/components/ui/EmptyState';
import { LoadingState } from '@/components/ui/LoadingState';
import { getVendors } from '@/lib/api';
import { BANGALORE_CENTER } from '@/lib/constants';
import type { Vendor } from '@/lib/types';

const VendorMap = dynamic(() => import('@/components/map/VendorMap').then((module) => module.VendorMap), {
  ssr: false,
  loading: () => <div className="h-screen bg-orange-100" />,
});

export default function MapPage() {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | undefined>();
  const [locating, setLocating] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    function load(location?: { lat: number; lng: number }) {
      setLoading(true);
      getVendors({
        lat: location?.lat,
        lng: location?.lng,
        limit: 100,
      })
        .then((response) => {
          if (alive) {
            setVendors(response.vendors);
            setError(null);
          }
        })
        .catch((requestError: unknown) => {
          if (alive) {
            setError(requestError instanceof Error ? requestError.message : 'Unable to load map vendors');
          }
        })
        .finally(() => {
          if (alive) {
            setLoading(false);
            setLocating(false);
          }
        });
    }

    if (!navigator.geolocation) {
      load();
      return () => {
        alive = false;
      };
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location = { lat: position.coords.latitude, lng: position.coords.longitude };
        if (alive) {
          setUserLocation(location);
        }
        load(location);
      },
      () => load(),
      { enableHighAccuracy: true, timeout: 8000 },
    );

    return () => {
      alive = false;
    };
  }, []);

  if (loading) {
    return <div className="h-screen p-4"><LoadingState message="Loading map vendors..." /></div>;
  }

  if (error) {
    return <div className="mx-auto max-w-3xl px-4 py-16"><EmptyState title="Could not load map" description={error} /></div>;
  }

  return (
    <div className="relative h-screen">
      {locating ? (
        <div className="absolute left-1/2 top-4 z-[500] -translate-x-1/2 rounded-full bg-white px-4 py-2 text-sm font-bold text-secondary shadow-md">
          Locating you...
        </div>
      ) : null}
      <VendorMap
        vendors={vendors}
        userLocation={userLocation}
        center={userLocation ?? BANGALORE_CENTER}
        height="100%"
      />
    </div>
  );
}
