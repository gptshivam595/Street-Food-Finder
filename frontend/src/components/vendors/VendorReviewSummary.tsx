import { Rating } from '@/components/ui/Rating';
import type { Vendor } from '@/lib/types';

interface VendorReviewSummaryProps {
  vendor: Vendor;
}

export function VendorReviewSummary({ vendor }: VendorReviewSummaryProps) {
  return (
    <div className="grid gap-3 rounded-2xl bg-white p-4 shadow-sm sm:grid-cols-3">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Overall</p>
        <div className="mt-1 flex items-center gap-2">
          <Rating value={vendor.average_rating} size="sm" />
          <span className="font-bold text-secondary">{vendor.average_rating.toFixed(1)}</span>
        </div>
      </div>
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Hygiene</p>
        <div className="mt-1 flex items-center gap-2">
          <Rating value={vendor.hygiene_rating} size="sm" />
          <span className="font-bold text-secondary">{vendor.hygiene_rating.toFixed(1)}</span>
        </div>
      </div>
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Reviews</p>
        <p className="mt-1 text-lg font-bold text-secondary">{vendor.review_count}</p>
      </div>
    </div>
  );
}
