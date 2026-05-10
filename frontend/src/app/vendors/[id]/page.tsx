'use client';

import dynamic from 'next/dynamic';
import { FormEvent, useEffect, useMemo, useState } from 'react';

import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { EmptyState } from '@/components/ui/EmptyState';
import { Input } from '@/components/ui/Input';
import { LoadingState } from '@/components/ui/LoadingState';
import { Rating } from '@/components/ui/Rating';
import { VendorReviewSummary } from '@/components/vendors/VendorReviewSummary';
import { VendorStatusBadge } from '@/components/vendors/VendorStatusBadge';
import { createReview, getVendorById, getVendorReviews } from '@/lib/api';
import { VENDOR_ZOOM } from '@/lib/constants';
import type { Review, ReviewCreate, Vendor } from '@/lib/types';
import { formatTime, getCategoryEmoji, getDirectionsUrl } from '@/lib/utils';

const VendorMap = dynamic(() => import('@/components/map/VendorMap').then((module) => module.VendorMap), {
  ssr: false,
  loading: () => <div className="h-[250px] rounded-2xl bg-orange-100" />,
});

interface PageProps {
  params: { id: string };
}

export default function VendorDetailPage({ params }: PageProps) {
  const [vendor, setVendor] = useState<Vendor | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState<ReviewCreate>({
    user_name: '',
    rating: 5,
    hygiene_rating: 5,
    comment: '',
  });

  useEffect(() => {
    let alive = true;
    async function load() {
      try {
        setLoading(true);
        const [vendorData, reviewData] = await Promise.all([
          getVendorById(params.id),
          getVendorReviews(params.id),
        ]);
        if (!alive) {
          return;
        }
        setVendor(vendorData);
        setReviews(reviewData.reviews);
        setError(null);
      } catch (requestError) {
        if (alive) {
          setError(requestError instanceof Error ? requestError.message : 'Vendor not found');
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
  }, [params.id]);

  const groupedItems = useMemo(() => {
    const groups = new Map<string, NonNullable<Vendor['food_items']>>();
    for (const item of vendor?.food_items ?? []) {
      const existing = groups.get(item.category) ?? [];
      existing.push(item);
      groups.set(item.category, existing);
    }
    return Array.from(groups.entries());
  }, [vendor?.food_items]);

  async function submitReview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!vendor) {
      return;
    }
    setSubmitting(true);
    setSubmitError(null);
    setSuccess(null);
    try {
      const review = await createReview(vendor.id, form);
      setReviews((current) => [review, ...current]);
      const updatedVendor = await getVendorById(vendor.id);
      setVendor(updatedVendor);
      setForm({ user_name: '', rating: 5, hygiene_rating: 5, comment: '' });
      setSuccess('Review added successfully.');
    } catch (requestError) {
      setSubmitError(requestError instanceof Error ? requestError.message : 'Could not add review');
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8"><LoadingState /></div>;
  }

  if (error || !vendor) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
        <EmptyState title="Vendor not found" description={error ?? 'This vendor is not available.'} />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
      <section className="rounded-2xl bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <VendorStatusBadge isOpen={vendor.is_open_now} />
            <h1 className="mt-4 text-3xl font-extrabold text-secondary sm:text-4xl">{vendor.name}</h1>
            <p className="mt-2 font-semibold text-slate-700">{vendor.area}</p>
            <p className="mt-1 max-w-3xl text-sm text-slate-600">{vendor.address}</p>
            <p className="mt-3 text-sm font-semibold text-slate-700">
              {formatTime(vendor.opening_time)} – {formatTime(vendor.closing_time)}
            </p>
            {vendor.phone ? <p className="mt-2 text-sm text-slate-600">{vendor.phone}</p> : null}
          </div>
          <a href={getDirectionsUrl(vendor.latitude, vendor.longitude)} target="_blank" rel="noreferrer" className="rounded-full bg-primary px-5 py-3 text-center font-bold text-white transition hover:bg-primary/90">
            Get Directions
          </a>
        </div>
      </section>

      <VendorReviewSummary vendor={vendor} />

      <section className="grid gap-8 lg:grid-cols-[1fr_380px]">
        <div className="space-y-8">
          <Card>
            <h2 className="text-2xl font-extrabold text-secondary">Food Items</h2>
            <div className="mt-5 space-y-6">
              {groupedItems.map(([category, items]) => (
                <div key={category}>
                  <h3 className="mb-3 font-bold text-secondary">{getCategoryEmoji(category)} {category}</h3>
                  <div className="divide-y divide-orange-100 overflow-hidden rounded-2xl border border-orange-100">
                    {items.map((item) => (
                      <div key={item.id} className="flex items-center justify-between gap-4 bg-white p-4">
                        <div>
                          <p className="font-semibold text-secondary">{item.name}</p>
                          <p className="text-sm text-slate-500">₹{item.price}</p>
                        </div>
                        <Badge tone={item.is_available ? 'success' : 'danger'}>
                          {item.is_available ? 'Available' : 'Unavailable'}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <h2 className="text-2xl font-extrabold text-secondary">Reviews</h2>
            <form onSubmit={submitReview} className="mt-5 space-y-4 rounded-2xl bg-background p-4">
              <Input
                required
                placeholder="Your name"
                value={form.user_name}
                onChange={(event) => setForm((current) => ({ ...current, user_name: event.target.value }))}
              />
              <div className="grid gap-4 sm:grid-cols-2">
                <label className="space-y-2 text-sm font-bold text-secondary">
                  Overall rating
                  <Rating interactive value={form.rating} onChange={(rating) => setForm((current) => ({ ...current, rating }))} />
                </label>
                <label className="space-y-2 text-sm font-bold text-secondary">
                  Hygiene rating
                  <Rating interactive value={form.hygiene_rating} onChange={(hygiene_rating) => setForm((current) => ({ ...current, hygiene_rating }))} />
                </label>
              </div>
              <textarea
                value={form.comment}
                onChange={(event) => setForm((current) => ({ ...current, comment: event.target.value }))}
                placeholder="Share what stood out"
                className="min-h-28 w-full rounded-2xl border border-orange-100 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-4 focus:ring-primary/10"
              />
              {submitError ? <p className="text-sm font-semibold text-red-600">{submitError}</p> : null}
              {success ? <p className="text-sm font-semibold text-green-700">{success}</p> : null}
              <Button type="submit" disabled={submitting}>
                {submitting ? 'Submitting...' : 'Submit Review'}
              </Button>
            </form>
            <div className="mt-6 space-y-4">
              {reviews.map((review) => (
                <div key={review.id} className="rounded-2xl border border-orange-100 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <p className="font-bold text-secondary">{review.user_name}</p>
                    <div className="flex items-center gap-3 text-sm font-semibold text-slate-700">
                      <span>⭐ {review.rating.toFixed(1)}</span>
                      <span>🧼 {review.hygiene_rating.toFixed(1)}</span>
                    </div>
                  </div>
                  {review.comment ? <p className="mt-2 text-sm text-slate-600">{review.comment}</p> : null}
                </div>
              ))}
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <h2 className="mb-4 text-xl font-extrabold text-secondary">Map Preview</h2>
            <VendorMap
              vendors={[vendor]}
              center={{ lat: vendor.latitude, lng: vendor.longitude }}
              zoom={VENDOR_ZOOM}
              height="250px"
            />
          </Card>
        </div>
      </section>
    </div>
  );
}
