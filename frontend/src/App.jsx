import React, { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Navbar from './components/layout/Navbar'
import LandingPage from './pages/LandingPage'
import AuthPage from './pages/AuthPage'
import TripBuilder from './pages/TripBuilder'
import ItineraryView from './pages/ItineraryView'
import Dashboard from './pages/Dashboard'
import { useAuthStore } from './store/authStore'

import ProtectedRoute from './components/common/ProtectedRoute'

export default function App() {
  const { initialize } = useAuthStore()

  useEffect(() => {
    initialize()
  }, [initialize])

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/builder" element={<TripBuilder />} />
          <Route path="/itinerary" element={<ItineraryView />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </main>
      <Toaster 
        position="top-right"
        toastOptions={{
          style: {
            borderRadius: '16px',
            background: '#0f172a',
            color: '#fff',
            fontSize: '13px',
            fontWeight: '600'
          }
        }} 
      />
    </div>
  )
}
