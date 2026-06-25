'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Redirect to login page
    router.push('/login')
  }, [router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-blue-600 mb-4">INTEGRATY</h1>
        <p className="text-gray-600">AI Usage Monitoring Platform</p>
        <p className="text-sm text-gray-400 mt-2">Redirecting...</p>
      </div>
    </div>
  )
}
