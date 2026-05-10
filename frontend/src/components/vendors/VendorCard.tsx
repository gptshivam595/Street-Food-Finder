import Link from 'next/link';

import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
import { formatDistance, formatTime, getCategoryEmoji, getDirectionsUrl } from '@/lib/utils';
import type { Vendor } from '@/lib/types';

import { VendorStatusBadge } from './VendorStatusBadge';

interface VendorCardProps {
  vendor: Vendor;
  showDistance?: boolean;
}

export function VendorCard({ vendor, showDistance = false }: VendorCardProps) {
  const items = vendor.food_items ?? [];
  const categories = Array.from(new Set(items.map((item) => item.category)));
  const visibleCategories = categories.slice(0, 3);
  const remaining = categories.length - visibleCategories.length;
  const popularItems = items.slice(0, 3);

  return (
    <Card className="flex h-full flex-col">
      <div className="flex items-start justify-between gap-3">
        <VendorStatusBadge isOpen={vendor.is_open_now} />
        {showDistance && vendor.distance_km !== null ? (
          <span className="text-xs font-bold text-primary">{formatDistance(vendor.distance_km)}</span>
        ) : null}
      </div>
      <div className="mt-4 flex-1">
        <h3 className="text-lg font-bold text-secondary">{vendor.name}</h3>
        <p className="mt-1 text-sm text-slate-600">📍 {vendor.area}</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {visibleCategories.map((category) => (
            <Badge key={category} tone="accent">
              {getCategoryEmoji(category)} {category}
            </Badge>
          ))}
          {remaining > 0 ? <Badge>+{remaining} more</Badge> : null}
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-3 text-sm font-semibold text-slate-700">
          <span>⭐ {vendor.average_rating.toFixed(1)}</span>
          <span>🧼 {vendor.hygiene_rating.toFixed(1)}</span>
        </div>
        <p className="mt-3 text-sm text-slate-600">
          {formatTime(vendor.opening_time)} – {formatTime(vendor.closing_time)}
        </p>
        {popularItems.length > 0 ? (
          <ul className="mt-4 space-y-2 text-sm text-slate-700">
            {popularItems.map((item) => (
              <li key={item.id} className="flex items-center justify-between gap-3">
                <span>{item.name}</span>
                <span className="font-bold text-secondary">₹{item.price}</span>
              </li>
            ))}
          </ul>
        ) : null}
      </div>
      <div className="mt-5 flex items-center justify-between border-t border-orange-100 pt-4 text-sm font-bold">
        <Link href={`/vendors/${vendor.id}`} className="text-primary hover:underline">
          View Details
        </Link>
        <a href={getDirectionsUrl(vendor.latitude, vendor.longitude)} target="_blank" rel="noreferrer" className="text-secondary hover:text-primary">
          Directions
        </a>
      </div>
    </Card>
  );
}
