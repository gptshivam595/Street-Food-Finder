import axios from 'axios';

import type {
  FoodItem,
  Review,
  ReviewCreate,
  ReviewListResponse,
  Vendor,
  VendorFilters,
  VendorListResponse,
} from './types';

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error('NEXT_PUBLIC_API_BASE_URL is not configured');
}

const api = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
});

function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError<{ detail?: string; message?: string }>(error)) {
    const data = error.response?.data;
    return data?.detail ?? data?.message ?? error.message ?? 'Something went wrong';
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'Something went wrong';
}

export async function getVendors(filters: VendorFilters = {}): Promise<VendorListResponse> {
  try {
    const response = await api.get<VendorListResponse>('/api/v1/vendors', { params: filters });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getVendorById(id: string): Promise<Vendor> {
  try {
    const response = await api.get<Vendor>(`/api/v1/vendors/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getVendorReviews(
  vendorId: string,
  limit = 20,
  offset = 0,
): Promise<ReviewListResponse> {
  try {
    const response = await api.get<ReviewListResponse>(`/api/v1/vendors/${vendorId}/reviews`, {
      params: { limit, offset },
    });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function createReview(vendorId: string, data: ReviewCreate): Promise<Review> {
  try {
    const response = await api.post<Review>(`/api/v1/vendors/${vendorId}/reviews`, data);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getVendorFoodItems(vendorId: string): Promise<FoodItem[]> {
  try {
    const response = await api.get<FoodItem[]>(`/api/v1/vendors/${vendorId}/food-items`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}
