export interface FoodItem {
  id: string;
  vendor_id: string;
  name: string;
  category: string;
  price: number;
  is_available: boolean;
}

export interface Review {
  id: string;
  vendor_id: string;
  user_name: string;
  rating: number;
  hygiene_rating: number;
  comment: string | null;
  created_at: string;
}

export interface Vendor {
  id: string;
  name: string;
  description: string | null;
  owner_name: string;
  phone: string | null;
  area: string;
  address: string;
  latitude: number;
  longitude: number;
  opening_time: string;
  closing_time: string;
  is_active: boolean;
  hygiene_rating: number;
  average_rating: number;
  review_count: number;
  is_open_now: boolean;
  distance_km: number | null;
  food_items?: FoodItem[];
  created_at: string;
  updated_at: string;
}

export interface VendorListResponse {
  vendors: Vendor[];
  total: number;
  limit: number;
  offset: number;
}

export interface ReviewListResponse {
  reviews: Review[];
  total: number;
  limit: number;
  offset: number;
}

export interface ReviewCreate {
  user_name: string;
  rating: number;
  hygiene_rating: number;
  comment: string;
}

export type VendorCategory =
  | 'Chaat' | 'Momos' | 'Dosa' | 'Idli/Vada' | 'Rolls'
  | 'Pav Bhaji' | 'Sandwich' | 'Tea/Coffee' | 'Juice'
  | 'Desserts' | 'Snacks';

export interface VendorFilters {
  q?: string;
  category?: string;
  lat?: number;
  lng?: number;
  radius_km?: number;
  open_now?: boolean;
  limit?: number;
  offset?: number;
}
