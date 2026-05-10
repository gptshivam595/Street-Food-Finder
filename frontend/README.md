# Street Food Finder Frontend

Next.js 14 frontend for browsing Bangalore street food vendors, filtering by category and timing, submitting reviews, and viewing vendors on a Leaflet map.

## Setup

```bash
cp .env.example .env.local
npm install
npm run dev
```

## Environment

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Build

```bash
npm run build
```

## Deployment

Deploy the `frontend` directory to Vercel and set `NEXT_PUBLIC_API_BASE_URL` to the Render backend URL.
