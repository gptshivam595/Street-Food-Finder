'use client';

import { useEffect, useState } from 'react';

import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { FOOD_CATEGORIES } from '@/lib/constants';
import { getCategoryEmoji } from '@/lib/utils';

interface VendorFiltersProps {
  search: string;
  category: string;
  openNow: boolean;
  sort: 'Rating' | 'Distance';
  hasLocation: boolean;
  loadingLocation: boolean;
  onSearchChange: (value: string) => void;
  onCategoryChange: (value: string) => void;
  onOpenNowChange: (value: boolean) => void;
  onSortChange: (value: 'Rating' | 'Distance') => void;
  onUseLocation: () => void;
}

export function VendorFilters({
  search,
  category,
  openNow,
  sort,
  hasLocation,
  loadingLocation,
  onSearchChange,
  onCategoryChange,
  onOpenNowChange,
  onSortChange,
  onUseLocation,
}: VendorFiltersProps) {
  const [localSearch, setLocalSearch] = useState(search);

  useEffect(() => {
    setLocalSearch(search);
  }, [search]);

  useEffect(() => {
    const handle = window.setTimeout(() => onSearchChange(localSearch), 400);
    return () => window.clearTimeout(handle);
  }, [localSearch, onSearchChange]);

  return (
    <aside className="space-y-5 rounded-2xl border border-orange-100 bg-white p-4 shadow-sm">
      <div>
        <label className="mb-2 block text-sm font-bold text-secondary" htmlFor="vendor-search">
          Search
        </label>
        <Input
          id="vendor-search"
          value={localSearch}
          onChange={(event) => setLocalSearch(event.target.value)}
          placeholder="Dosa, HSR, chaat..."
        />
      </div>

      <div>
        <p className="mb-2 text-sm font-bold text-secondary">Category</p>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => onCategoryChange('')}
            className={`rounded-full px-3 py-2 text-xs font-bold transition ${category === '' ? 'bg-primary text-white' : 'bg-background text-slate-700 hover:bg-orange-100'}`}
          >
            All
          </button>
          {FOOD_CATEGORIES.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => onCategoryChange(item)}
              className={`rounded-full px-3 py-2 text-xs font-bold transition ${category === item ? 'bg-primary text-white' : 'bg-background text-slate-700 hover:bg-orange-100'}`}
            >
              {getCategoryEmoji(item)} {item}
            </button>
          ))}
        </div>
      </div>

      <label className="flex cursor-pointer items-center justify-between gap-4 rounded-2xl bg-background p-3 text-sm font-bold text-secondary">
        Open Now
        <input
          type="checkbox"
          checked={openNow}
          onChange={(event) => onOpenNowChange(event.target.checked)}
          className="h-5 w-5 accent-primary"
        />
      </label>

      <div>
        <p className="mb-2 text-sm font-bold text-secondary">Sort</p>
        <div className="grid grid-cols-2 gap-2 rounded-full bg-background p-1">
          {(['Rating', 'Distance'] as const).map((option) => (
            <button
              key={option}
              type="button"
              disabled={option === 'Distance' && !hasLocation}
              onClick={() => onSortChange(option)}
              className={`rounded-full px-3 py-2 text-sm font-bold transition disabled:cursor-not-allowed disabled:opacity-40 ${sort === option ? 'bg-white text-primary shadow-sm' : 'text-slate-600'}`}
            >
              {option}
            </button>
          ))}
        </div>
      </div>

      <Button type="button" variant="outline" className="w-full" onClick={onUseLocation} disabled={loadingLocation}>
        {loadingLocation ? 'Locating...' : hasLocation ? 'Update my location' : 'Use my location'}
      </Button>
    </aside>
  );
}
