# Integraty Web Dashboard

Teacher/Administrator web dashboard for managing monitoring sessions.

## Setup

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Features

- Teacher/Admin authentication
- Create and manage students
- Schedule monitoring sessions
- Live session monitoring
- View reports and analytics
- Organization management

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Query
- Axios

## Deploy

Deploy to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/minuttt/Integraty)

## Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

For production:

```env
NEXT_PUBLIC_API_URL=https://api.integraty.com
```
