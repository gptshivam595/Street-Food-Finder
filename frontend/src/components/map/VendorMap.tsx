'use client';

import Link from 'next/link';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { CircleMarker, MapContainer, Marker, Popup, TileLayer, Tooltip } from 'react-leaflet';

import { BANGALORE_CENTER, DEFAULT_ZOOM } from '@/lib/constants';
import type { Vendor } from '@/lib/types';

interface LeafletIconPrototype extends L.Icon.Default {
  _getIconUrl?: () => string;
}

delete (L.Icon.Default.prototype as LeafletIconPrototype)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

interface VendorMapProps {
  vendors: Vendor[];
  userLocation?: { lat: number; lng: number };
  center?: { lat: number; lng: number };
  zoom?: number;
  height?: string;
}

export function VendorMap({
  vendors,
  userLocation,
  center,
  zoom = DEFAULT_ZOOM,
  height = '100%',
}: VendorMapProps) {
  const mapCenter = center ?? userLocation ?? BANGALORE_CENTER;

  return (
    <div style={{ height }} className="overflow-hidden rounded-2xl border border-orange-100">
      <MapContainer center={[mapCenter.lat, mapCenter.lng]} zoom={zoom} scrollWheelZoom className="h-full w-full">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {userLocation ? (
          <CircleMarker
            center={[userLocation.lat, userLocation.lng]}
            radius={9}
            pathOptions={{ color: '#2563EB', fillColor: '#3B82F6', fillOpacity: 0.85 }}
          >
            <Tooltip permanent direction="top">
              You are here
            </Tooltip>
          </CircleMarker>
        ) : null}
        {vendors.map((vendor) => (
          <Marker key={vendor.id} position={[vendor.latitude, vendor.longitude]}>
            <Popup>
              <div className="min-w-44 space-y-2">
                <p className="font-bold text-slate-900">{vendor.name}</p>
                <p className={vendor.is_open_now ? 'font-semibold text-green-700' : 'font-semibold text-red-700'}>
                  {vendor.is_open_now ? 'Open Now' : 'Closed'}
                </p>
                <p>Rating {vendor.average_rating.toFixed(1)}</p>
                <Link href={`/vendors/${vendor.id}`} className="font-semibold text-orange-600">
                  View Details
                </Link>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
