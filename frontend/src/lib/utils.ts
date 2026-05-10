export function formatTime(timeStr: string): string {
  const [hourPart, minutePart] = timeStr.split(':');
  const hour = Number(hourPart);
  const minute = Number(minutePart);
  const suffix = hour >= 12 ? 'PM' : 'AM';
  const hour12 = hour % 12 || 12;
  return `${hour12}:${minute.toString().padStart(2, '0')} ${suffix}`;
}

export function formatDistance(km: number): string {
  if (km < 1) {
    return `${Math.round(km * 1000)} m`;
  }
  return `${km.toFixed(1)} km`;
}

export function getDirectionsUrl(lat: number, lng: number): string {
  return `https://www.openstreetmap.org/directions?to=${lat},${lng}`;
}

export function getCategoryEmoji(category: string): string {
  const map: Record<string, string> = {
    Chaat: '🍛',
    Momos: '🥟',
    Dosa: '🫓',
    'Idli/Vada': '🍽️',
    Rolls: '🌯',
    'Pav Bhaji': '🥘',
    Sandwich: '🥪',
    'Tea/Coffee': '☕',
    Juice: '🧃',
    Desserts: '🍮',
    Snacks: '🍟',
  };
  return map[category] ?? '🍴';
}

export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(' ');
}
