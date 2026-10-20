import React, { useState, useEffect } from 'react'
import { Sparkles, MapPin, Compass } from 'lucide-react'

const LOADING_MESSAGES = [
  'Scouting the best local attractions... 🔍',
  'Optimizing your daily routes to save travel time... 🗺️',
  'Curating authentic dining and street food spots... 🍽️',
  'Balancing day-by-day activities within your budget... 💰',
  'Adding hidden gems and practical travel tips... ✨',
  'Putting the finishing touches on your itinerary... 🎒'
]

export default function LoadingScreen({ onCancel }) {
  const [messageIndex, setMessageIndex] = useState(0)
  const [showCancel, setShowCancel] = useState(false)

  useEffect(() => {
    const messageInterval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length)
    }, 2800)

    const cancelTimeout = setTimeout(() => {
      setShowCancel(true)
    }, 10000)

    return () => {
      clearInterval(messageInterval)
      clearTimeout(cancelTimeout)
    }
  }, [])

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl border border-slate-100 flex flex-col items-center text-center animate-in fade-in zoom-in duration-300">
        {/* Animated Compass Icon */}
        <div className="relative mb-6">
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-sky-100 to-indigo-100 flex items-center justify-center animate-pulse">
            <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-300">
              <Compass className="w-9 h-9 text-white animate-spin" style={{ animationDuration: '6s' }} />
            </div>
          </div>
          <div className="absolute -top-1 -right-1 bg-amber-400 text-amber-950 p-1.5 rounded-full shadow-md animate-bounce">
            <Sparkles className="w-4 h-4" />
          </div>
        </div>

        <h3 className="text-xl font-bold text-slate-900 mb-2">
          Generating Your Custom Itinerary
        </h3>

        {/* Rotating Message */}
        <div className="h-12 flex items-center justify-center">
          <p className="text-sm font-medium text-sky-700 transition-all duration-500 ease-in-out">
            {LOADING_MESSAGES[messageIndex]}
          </p>
        </div>

        {/* Progress Bar Animation */}
        <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden mt-4 mb-6">
          <div className="bg-gradient-to-r from-sky-500 to-indigo-600 h-full rounded-full animate-[progress_2s_ease-in-out_infinite]" />
        </div>

        <p className="text-xs text-slate-400 mb-6">
          Powered by LLaMA 3.3 via Groq API
        </p>

        {showCancel && (
          <button
            onClick={onCancel}
            className="text-xs font-semibold text-slate-400 hover:text-red-500 transition underline underline-offset-4"
          >
            Taking too long? Cancel generation
          </button>
        )}
      </div>
    </div>
  )
}
