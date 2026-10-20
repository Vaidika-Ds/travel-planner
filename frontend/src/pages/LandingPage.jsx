import React from 'react'
import { Link } from 'react-router-dom'
import { Sparkles, MapPin, Compass, ShieldCheck, Clock, Zap, ArrowRight, Heart } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-between">
      {/* Hero Section */}
      <div className="relative overflow-hidden pt-12 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto text-center">
          
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sky-100 text-sky-800 font-semibold text-xs mb-8 shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-sky-600" />
            <span>AI-Powered Itinerary Creator • Instant & Tailored</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-black text-slate-900 tracking-tight leading-tight sm:leading-none">
            Your Dream Vacation,{' '}
            <span className="bg-gradient-to-r from-sky-600 to-indigo-600 bg-clip-text text-transparent">
              Planned in Seconds
            </span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Stop spending hours researching hotels, routes, and attractions. Tell us your destination, budget, and vibe — our AI crafts the perfect day-by-day plan.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/builder"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl bg-gradient-to-r from-sky-600 to-indigo-600 text-white font-extrabold text-base hover:from-sky-700 hover:to-indigo-700 shadow-xl shadow-sky-200 transition"
            >
              <span>Build My Itinerary Free</span>
              <ArrowRight className="w-5 h-5" />
            </Link>

            <Link
              to="/auth"
              className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-4 rounded-2xl bg-white border border-slate-200 text-slate-700 font-bold text-base hover:bg-slate-50 transition shadow-sm"
            >
              Sign In to View Trips
            </Link>
          </div>

          {/* Feature Badges */}
          <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6 text-left">
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
              <div className="w-12 h-12 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center mb-4">
                <Zap className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg mb-1">Sub-Second AI Plans</h3>
              <p className="text-sm text-slate-500">
                Powered by Groq's LPU architecture, itineraries generate in seconds, not minutes.
              </p>
            </div>

            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
              <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg mb-1">Budget Optimized</h3>
              <p className="text-sm text-slate-500">
                Every activity, hotel, and meal is calculated to stay strictly within your budget ceiling.
              </p>
            </div>

            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
              <div className="w-12 h-12 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center mb-4">
                <Compass className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 text-lg mb-1">Fully Editable</h3>
              <p className="text-sm text-slate-500">
                Customize, remove, or adjust activities anytime, then export or share with your companions.
              </p>
            </div>
          </div>

        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-200 py-6 text-center text-xs text-slate-400">
        <p>© 2026 VoyageAI — Personalized Travel Itinerary Planner. Built with React, FastAPI & Groq.</p>
      </footer>
    </div>
  )
}
