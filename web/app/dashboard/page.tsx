'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token')
    const userData = localStorage.getItem('user')

    if (!token || !userData) {
      router.push('/login')
      return
    }

    setUser(JSON.parse(userData))
    setLoading(false)
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-blue-600">INTEGRATY</h1>
            <p className="text-sm text-gray-600">Welcome, {user?.full_name}</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
          <p className="text-gray-600 mt-1">Manage your monitoring sessions</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <p className="text-sm text-gray-600">Total Students</p>
            <p className="text-3xl font-bold text-blue-600 mt-2">0</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <p className="text-sm text-gray-600">Active Sessions</p>
            <p className="text-3xl font-bold text-green-600 mt-2">0</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <p className="text-sm text-gray-600">Total Sessions</p>
            <p className="text-3xl font-bold text-purple-600 mt-2">0</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <p className="text-sm text-gray-600">Detections</p>
            <p className="text-3xl font-bold text-red-600 mt-2">0</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="p-4 border-2 border-blue-200 rounded-lg hover:bg-blue-50 text-left transition-colors">
              <div className="text-2xl mb-2">📝</div>
              <div className="font-medium text-gray-900">Create Session</div>
              <div className="text-sm text-gray-600">Start a new monitoring session</div>
            </button>

            <button className="p-4 border-2 border-green-200 rounded-lg hover:bg-green-50 text-left transition-colors">
              <div className="text-2xl mb-2">👥</div>
              <div className="font-medium text-gray-900">Manage Students</div>
              <div className="text-sm text-gray-600">Add or edit student accounts</div>
            </button>

            <button className="p-4 border-2 border-purple-200 rounded-lg hover:bg-purple-50 text-left transition-colors">
              <div className="text-2xl mb-2">📊</div>
              <div className="font-medium text-gray-900">View Reports</div>
              <div className="text-sm text-gray-600">Check session analytics</div>
            </button>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <p className="text-gray-500 text-center py-8">No recent activity</p>
        </div>

        {/* Coming Soon Notice */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h4 className="font-semibold text-blue-900 mb-2">🚧 Dashboard Under Development</h4>
          <p className="text-sm text-blue-800">
            Full dashboard features coming soon! This is the landing page after login.
            Features to be added: Session management, Student management, Live monitoring, Report generation.
          </p>
        </div>
      </main>
    </div>
  )
}
