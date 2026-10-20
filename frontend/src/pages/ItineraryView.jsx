import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { 
  Calendar, MapPin, DollarSign, Clock, Lightbulb, 
  Share2, Download, ArrowLeft, CheckCircle2, Utensils, 
  Camera, Car, Bed, Sparkles, AlertCircle, Edit3, Trash2,
  RefreshCw, X, Check
} from 'lucide-react'
import { useTripStore } from '../store/tripStore'
import { regenerateDayAPI } from '../services/api'
import toast from 'react-hot-toast'

export default function ItineraryView() {
  const navigate = useNavigate()
  const { currentItinerary, formData } = useTripStore()

  // State to hold itinerary allowing local edits
  const [itinerary, setItinerary] = useState(currentItinerary)
  const [activeDayIndex, setActiveDayIndex] = useState(0)
  const [isRegeneratingDay, setIsRegeneratingDay] = useState(false)

  // Edit Modal State
  const [editingActivity, setEditingActivity] = useState(null) // { dayNumber, actIndex, activity }

  if (!itinerary) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center p-4 text-center">
        <div className="w-16 h-16 rounded-full bg-sky-50 text-sky-600 flex items-center justify-center mb-4">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-bold text-slate-800 mb-2">No Active Itinerary Found</h2>
        <p className="text-sm text-slate-500 max-w-sm mb-6">
          You haven't generated a trip plan yet. Start with our trip builder!
        </p>
        <Link
          to="/builder"
          className="px-6 py-2.5 rounded-xl font-semibold bg-sky-600 text-white hover:bg-sky-700 shadow-md transition"
        >
          Plan a Trip Now
        </Link>
      </div>
    )
  }

  const days = itinerary.days || []
  const activeDay = days[activeDayIndex] || days[0]

  const getActivityIcon = (type) => {
    switch (type) {
      case 'dining': return <Utensils className="w-4 h-4 text-amber-600" />
      case 'travel': return <Car className="w-4 h-4 text-indigo-600" />
      case 'accommodation': return <Bed className="w-4 h-4 text-purple-600" />
      default: return <Camera className="w-4 h-4 text-sky-600" />
    }
  }

  // Delete Activity
  const handleDeleteActivity = (dayNumber, activityIndex) => {
    const updatedDays = itinerary.days.map((d) => {
      if (d.day_number === dayNumber) {
        return {
          ...d,
          activities: d.activities.filter((_, idx) => idx !== activityIndex)
        }
      }
      return d
    })
    setItinerary({ ...itinerary, days: updatedDays })
    toast.success('Activity removed')
  }

  // Edit Activity Save
  const handleSaveActivityEdit = (e) => {
    e.preventDefault()
    if (!editingActivity) return

    const { dayNumber, actIndex, activity } = editingActivity
    const updatedDays = itinerary.days.map((d) => {
      if (d.day_number === dayNumber) {
        const newActs = [...d.activities]
        newActs[actIndex] = { ...activity }
        return { ...d, activities: newActs }
      }
      return d
    })
    setItinerary({ ...itinerary, days: updatedDays })
    setEditingActivity(null)
    toast.success('Activity updated!')
  }

  // Regenerate Single Day (e.g. Day 2)
  const handleRegenerateDay = async () => {
    if (!activeDay) return
    setIsRegeneratingDay(true)
    const toastId = toast.loading(`Regenerating Day ${activeDay.day_number}...`)

    try {
      const payload = {
        destination: itinerary.destination || formData.destination,
        day_number: activeDay.day_number,
        day_date: activeDay.date || null,
        day_budget: Number(activeDay.estimated_day_cost) || 3000,
        currency: itinerary.currency || 'INR',
        travel_style: formData.travelStyle || 'moderate',
        interests: formData.interests || [],
        pace: formData.pace || 'moderate',
        existing_themes: days.map(d => d.theme).filter(Boolean)
      }

      const res = await regenerateDayAPI(payload)
      if (res.status === 'success' && res.day) {
        const updatedDays = itinerary.days.map((d) => {
          if (d.day_number === activeDay.day_number) {
            return {
              ...d,
              theme: res.day.theme || d.theme,
              estimated_day_cost: res.day.estimated_day_cost || d.estimated_day_cost,
              activities: res.day.activities || d.activities
            }
          }
          return d
        })
        setItinerary({ ...itinerary, days: updatedDays })
        toast.success(`Day ${activeDay.day_number} refreshed!`, { id: toastId })
      } else {
        throw new Error('Could not regenerate day')
      }
    } catch (err) {
      console.error(err)
      toast.error('Failed to regenerate this day. Please try again.', { id: toastId })
    } finally {
      setIsRegeneratingDay(false)
    }
  }

  const handleShare = () => {
    const shareUrl = `${window.location.origin}/itinerary`
    if (navigator.share) {
      navigator.share({
        title: itinerary.trip_title,
        text: `Check out my travel plan for ${itinerary.destination}!`,
        url: shareUrl,
      }).catch(() => {})
    } else {
      navigator.clipboard.writeText(shareUrl)
      toast.success('Trip link copied to clipboard!')
    }
  }

  const handleExportPDF = () => {
    window.print()
  }

  return (
    <div className="min-h-screen bg-slate-50 pb-28">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-sky-950 to-indigo-950 text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <Link
            to="/builder"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-300 hover:text-white mb-6 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Create Another Trip</span>
          </Link>

          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-500/20 text-sky-300 border border-sky-400/30 text-xs font-semibold mb-3">
                <Sparkles className="w-3.5 h-3.5" />
                <span>AI Personalized Plan</span>
              </div>
              <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
                {itinerary.trip_title}
              </h1>
              <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-slate-300 font-medium">
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-4 h-4 text-sky-400" />
                  {itinerary.destination}
                </span>
                <span>•</span>
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-4 h-4 text-sky-400" />
                  {itinerary.total_days} Days
                </span>
              </div>
            </div>

            {/* Cost Badges */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10 min-w-[220px]">
              <div className="text-xs text-slate-300 font-medium">Estimated Total Cost</div>
              <div className="text-2xl font-black text-white mt-0.5">
                {itinerary.currency} {Number(itinerary.estimated_total_cost).toLocaleString()}
              </div>
              <div className="text-[11px] text-sky-300 mt-1 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> Within {itinerary.currency} {Number(formData.budgetTotal || itinerary.estimated_total_cost).toLocaleString()} Budget
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        
        {/* Day Selector Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-4 scrollbar-none">
          {days.map((day, idx) => (
            <button
              key={day.day_number || idx}
              onClick={() => setActiveDayIndex(idx)}
              className={`px-5 py-3 rounded-2xl font-bold text-sm whitespace-nowrap transition flex items-center gap-2 ${
                activeDayIndex === idx
                  ? 'bg-sky-600 text-white shadow-md shadow-sky-200'
                  : 'bg-white text-slate-700 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <span>Day {day.day_number}</span>
              <span className={`text-xs px-2 py-0.5 rounded-full ${activeDayIndex === idx ? 'bg-sky-700 text-sky-100' : 'bg-slate-100 text-slate-500'}`}>
                {itinerary.currency} {day.estimated_day_cost}
              </span>
            </button>
          ))}
        </div>

        {/* Selected Day Content */}
        {activeDay && (
          <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200 mt-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100 mb-6">
              <div>
                <span className="text-xs font-bold text-sky-600 uppercase tracking-wider">
                  Day {activeDay.day_number}
                </span>
                <h2 className="text-2xl font-extrabold text-slate-900 mt-0.5">
                  {activeDay.theme || `Day ${activeDay.day_number} Adventures`}
                </h2>
              </div>
              
              <div className="flex items-center gap-2.5">
                <div className="text-sm font-semibold text-slate-600 bg-slate-50 px-3.5 py-2 rounded-xl border border-slate-200">
                  Day Budget: {itinerary.currency} {activeDay.estimated_day_cost}
                </div>
                {/* Single Day Regenerate Button */}
                <button
                  onClick={handleRegenerateDay}
                  disabled={isRegeneratingDay}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold transition border border-indigo-200 disabled:opacity-50"
                  title="Regenerate only this day's plan"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isRegeneratingDay ? 'animate-spin' : ''}`} />
                  <span>Regenerate Day {activeDay.day_number}</span>
                </button>
              </div>
            </div>

            {/* Activities Timeline */}
            <div className="space-y-6 relative before:absolute before:inset-0 before:left-5 before:w-0.5 before:bg-slate-100">
              {activeDay.activities?.map((act, actIdx) => (
                <div key={actIdx} className="relative flex items-start gap-4 group">
                  {/* Icon circle */}
                  <div className="w-10 h-10 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-center shrink-0 z-10 group-hover:border-sky-400 group-hover:bg-sky-50 transition">
                    {getActivityIcon(act.activity_type)}
                  </div>

                  {/* Activity Card */}
                  <div className="flex-1 bg-slate-50/70 hover:bg-slate-50 rounded-2xl p-5 border border-slate-200/80 transition group-hover:border-slate-300">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-bold text-slate-500 flex items-center gap-1">
                            <Clock className="w-3.5 h-3.5" />
                            {act.time_slot}
                          </span>
                          <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-slate-200 text-slate-700">
                            {act.activity_type}
                          </span>
                        </div>
                        <h4 className="text-lg font-bold text-slate-900">{act.name}</h4>
                        <p className="text-xs font-medium text-slate-500 flex items-center gap-1 mt-0.5">
                          <MapPin className="w-3.5 h-3.5 text-slate-400" />
                          {act.location}
                        </p>
                      </div>

                      <div className="text-right shrink-0 flex items-center gap-2">
                        <span className="text-sm font-extrabold text-slate-800">
                          {act.estimated_cost > 0 ? `${itinerary.currency} ${act.estimated_cost}` : 'Free'}
                        </span>
                        
                        {/* Edit Activity Button */}
                        <button
                          onClick={() => setEditingActivity({
                            dayNumber: activeDay.day_number,
                            actIndex: actIdx,
                            activity: { ...act }
                          })}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-sky-600 hover:bg-white transition"
                          title="Edit activity"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>

                        {/* Delete Activity Button */}
                        <button
                          onClick={() => handleDeleteActivity(activeDay.day_number, actIdx)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-white transition"
                          title="Remove activity"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    <p className="text-sm text-slate-600 mt-2.5 leading-relaxed">
                      {act.description}
                    </p>

                    {act.tips && (
                      <div className="mt-3 p-3 rounded-xl bg-amber-50/80 border border-amber-200/70 flex items-start gap-2 text-xs text-amber-900 font-medium">
                        <Lightbulb className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                        <span><strong>Tip:</strong> {act.tips}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* General Tips & Accommodation Suggestions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-200">
            <h3 className="font-extrabold text-slate-900 flex items-center gap-2 mb-2 text-base">
              <Car className="w-5 h-5 text-indigo-600" />
              <span>Getting Around</span>
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed font-medium">
              {itinerary.transport_tips || 'Use local taxis, auto-rickshaws, or metro for easy commuting.'}
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-200">
            <h3 className="font-extrabold text-slate-900 flex items-center gap-2 mb-2 text-base">
              <Bed className="w-5 h-5 text-purple-600" />
              <span>Recommended Stays</span>
            </h3>
            <div className="flex flex-wrap gap-1.5 mt-2">
              {itinerary.accommodation_suggestions?.map((stay, sIdx) => (
                <span key={sIdx} className="text-xs bg-purple-50 text-purple-800 border border-purple-200 px-3 py-1 rounded-xl font-medium">
                  {stay}
                </span>
              ))}
            </div>
          </div>
        </div>

      </div>

      {/* Sticky Bottom Bar */}
      <div className="fixed bottom-0 inset-x-0 bg-white/95 backdrop-blur-md border-t border-slate-200 py-3 px-4 sm:px-8 z-30 shadow-lg">
        <div className="max-w-5xl mx-auto flex items-center justify-between gap-4">
          <div className="hidden sm:block">
            <span className="text-xs text-slate-400 font-medium">Trip Summary</span>
            <div className="text-sm font-bold text-slate-800">
              {itinerary.destination} • {itinerary.total_days} Days
            </div>
          </div>

          <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
            <button
              onClick={handleShare}
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-slate-200 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
            >
              <Share2 className="w-4 h-4 text-slate-500" />
              <span>Share Trip</span>
            </button>

            <button
              onClick={handleExportPDF}
              className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-sky-600 text-white text-sm font-bold hover:bg-sky-700 shadow-md shadow-sky-200 transition"
            >
              <Download className="w-4 h-4" />
              <span>Save & Print PDF</span>
            </button>
          </div>
        </div>
      </div>

      {/* Edit Activity Modal */}
      {editingActivity && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-slate-900">Edit Activity</h3>
              <button 
                onClick={() => setEditingActivity(null)}
                className="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveActivityEdit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Activity Name</label>
                <input
                  type="text"
                  required
                  value={editingActivity.activity.name}
                  onChange={(e) => setEditingActivity({
                    ...editingActivity,
                    activity: { ...editingActivity.activity, name: e.target.value }
                  })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:border-sky-500 outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Time Slot</label>
                  <input
                    type="text"
                    value={editingActivity.activity.time_slot}
                    onChange={(e) => setEditingActivity({
                      ...editingActivity,
                      activity: { ...editingActivity.activity, time_slot: e.target.value }
                    })}
                    className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:border-sky-500 outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Cost ({itinerary.currency})</label>
                  <input
                    type="number"
                    value={editingActivity.activity.estimated_cost}
                    onChange={(e) => setEditingActivity({
                      ...editingActivity,
                      activity: { ...editingActivity.activity, estimated_cost: Number(e.target.value) }
                    })}
                    className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:border-sky-500 outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Description</label>
                <textarea
                  rows="3"
                  value={editingActivity.activity.description}
                  onChange={(e) => setEditingActivity({
                    ...editingActivity,
                    activity: { ...editingActivity.activity, description: e.target.value }
                  })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:border-sky-500 outline-none resize-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setEditingActivity(null)}
                  className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl text-sm font-bold bg-sky-600 text-white hover:bg-sky-700 shadow-md"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  )
}
