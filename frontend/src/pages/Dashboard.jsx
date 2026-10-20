import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { PlusCircle, Calendar, MapPin, Sparkles, AlertCircle, Eye, ArrowRight } from 'lucide-react'
import { fetchUserTripsAPI, fetchTripDetailsAPI } from '../services/api'
import { useTripStore } from '../store/tripStore'
import { useAuthStore } from '../store/authStore'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const { setItineraryResult } = useTripStore()
  const [trips, setTrips] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadTrips = async () => {
      try {
        const data = await fetchUserTripsAPI()
        setTrips(data || [])
      } catch (err) {
        console.error('Failed to load trips:', err)
      } finally {
        setLoading(false)
      }
    }
    loadTrips()
  }, [])

  const handleOpenTrip = async (trip) => {
    try {
      if (trip.itinerary) {
        setItineraryResult(trip.itinerary, trip.id)
        navigate('/itinerary')
      } else {
        const fullTrip = await fetchTripDetailsAPI(trip.id)
        if (fullTrip.itinerary) {
          setItineraryResult(fullTrip.itinerary, fullTrip.id)
          navigate('/itinerary')
        } else {
          toast.error('No itinerary found for this trip.')
        }
      }
    } catch (err) {
      console.error('Failed to load trip details:', err)
      toast.error('Could not open trip.')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900">My Trips</h1>
            <p className="text-sm text-slate-500 mt-1">Manage, revisit, and export your saved travel plans.</p>
          </div>

          <Link
            to="/builder"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-2xl bg-sky-600 text-white font-bold text-sm hover:bg-sky-700 shadow-md shadow-sky-200 transition"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Plan New Trip</span>
          </Link>
        </div>

        {/* Content */}
        {loading ? (
          <div className="py-20 text-center">
            <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-xs font-semibold text-slate-500">Loading your itineraries...</p>
          </div>
        ) : trips.length === 0 ? (
          <div className="bg-white rounded-3xl p-12 text-center border border-slate-200 shadow-sm max-w-lg mx-auto">
            <div className="w-16 h-16 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-1">No trips planned yet</h3>
            <p className="text-xs text-slate-500 mb-6">
              Use our AI builder to generate your first custom trip itinerary in seconds.
            </p>
            <Link
              to="/builder"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-sky-600 text-white text-sm font-bold hover:bg-sky-700 shadow-md transition"
            >
              <span>Create Your First Trip</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {trips.map((trip) => (
              <div
                key={trip.id}
                className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-xs font-bold text-sky-600 uppercase tracking-wider flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5" />
                      {trip.destination}
                    </span>
                    <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700">
                      {trip.num_days || 1} Days
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 line-clamp-1">
                    {trip.title || `Trip to ${trip.destination}`}
                  </h3>

                  <div className="flex items-center gap-4 text-xs text-slate-500 font-medium mt-2">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {trip.start_date}
                    </span>
                    <span>•</span>
                    <span>
                      Budget: {trip.currency} {Number(trip.budget_total).toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-400 capitalize">
                    {trip.travel_style || 'Relaxed'} • {trip.group_type || 'Solo'}
                  </span>

                  <button
                    onClick={() => handleOpenTrip(trip)}
                    className="inline-flex items-center gap-1 text-xs font-bold text-sky-600 hover:text-sky-700 transition"
                  >
                    <span>View Itinerary</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  )
}
