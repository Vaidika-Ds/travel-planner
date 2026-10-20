import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  MapPin, Calendar, Users, DollarSign, Sparkles, 
  ArrowRight, ArrowLeft, Heart, Compass, Shield, Flame, 
  Coffee, Gem, Wallet, AlertCircle
} from 'lucide-react'
import { useTripStore } from '../store/tripStore'
import { useAuthStore } from '../store/authStore'
import { generateItineraryAPI } from '../services/api'
import LoadingScreen from '../components/common/LoadingScreen'
import toast from 'react-hot-toast'

const TRAVEL_STYLES = [
  { id: 'relaxed', label: 'Relaxed', desc: 'Chill pacing, cozy cafes & sunsets', icon: Coffee },
  { id: 'cultural', label: 'Cultural & Historic', desc: 'Museums, monuments & local history', icon: Compass },
  { id: 'adventure', label: 'Adventure & Nature', desc: 'Treks, wildlife & outdoor thrills', icon: Flame },
  { id: 'romantic', label: 'Romantic', desc: 'Curated dining, scenic views & intimate spots', icon: Heart },
  { id: 'luxury', label: 'Luxury & Comfort', desc: 'Premium stays & fine dining', icon: Gem },
  { id: 'budget', label: 'Backpacker / Budget', desc: 'Smart spending & street food', icon: Wallet }
]

const INTEREST_TAGS = [
  'Historical Forts', 'Local Food & Street Food', 'Beaches', 'Museums',
  'Nightlife & Pubs', 'Shopping & Bazaars', 'Nature & Hiking', 'Photography Spots',
  'Temples & Spirituality', 'Art Galleries', 'Wellness & Spa', 'Wildlife'
]

const POPULAR_DESTINATIONS = [
  'Jaipur, Rajasthan', 'Goa, India', 'Manali, Himachal Pradesh', 
  'Kerala (Munnar & Alleppey)', 'Agra, Uttar Pradesh', 'Varanasi, Uttar Pradesh',
  'Paris, France', 'Dubai, UAE', 'Tokyo, Japan', 'Bali, Indonesia'
]

export default function TripBuilder() {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const { 
    formData, setFormField, isGenerating, 
    setGenerating, setItineraryResult, setError 
  } = useTripStore()

  const [step, setStep] = useState(1)
  const [formErrors, setFormErrors] = useState({})

  // Compute number of days
  const calculateDays = () => {
    if (!formData.startDate || !formData.endDate) return 0
    const start = new Date(formData.startDate)
    const end = new Date(formData.endDate)
    const diff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1
    return diff > 0 ? diff : 0
  }

  const numDays = calculateDays()
  const perDayBudget = numDays > 0 ? Math.round(formData.budgetTotal / numDays) : formData.budgetTotal

  // Step 1 validation
  const validateStep1 = () => {
    const errors = {}
    if (!formData.destination.trim()) errors.destination = 'Please enter a destination'
    if (!formData.startDate) errors.startDate = 'Select start date'
    if (!formData.endDate) errors.endDate = 'Select end date'
    if (formData.startDate && formData.endDate && new Date(formData.endDate) < new Date(formData.startDate)) {
      errors.endDate = 'End date cannot be before start date'
    }
    setFormErrors(errors)
    return Object.keys(errors).length === 0
  }

  // Step 2 validation
  const validateStep2 = () => {
    const errors = {}
    if (!formData.budgetTotal || formData.budgetTotal <= 0) {
      errors.budgetTotal = 'Please enter a valid budget'
    }
    if (formData.groupType === 'group' && (!formData.groupSize || formData.groupSize < 1)) {
      errors.groupSize = 'Group size must be at least 1'
    }
    setFormErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleNext = () => {
    if (step === 1 && validateStep1()) setStep(2)
    else if (step === 2 && validateStep2()) setStep(3)
  }

  const handleBack = () => {
    if (step > 1) setStep(step - 1)
  }

  const toggleInterest = (tag) => {
    const current = formData.interests || []
    if (current.includes(tag)) {
      setFormField('interests', current.filter((i) => i !== tag))
    } else {
      setFormField('interests', [...current, tag])
    }
  }

  const handleGenerate = async () => {
    if (!user) {
      toast.error('Please sign in or create an account to generate your itinerary!')
      navigate('/auth')
      return
    }

    setGenerating(true)
    try {
      const payload = {
        destination: formData.destination,
        start_date: formData.startDate,
        end_date: formData.endDate,
        budget_total: Number(formData.budgetTotal),
        currency: formData.currency,
        travel_style: formData.travelStyle,
        interests: formData.interests,
        group_type: formData.groupType,
        group_size: Number(formData.groupSize),
        accommodation_preference: formData.accommodationPreference,
        pace: formData.pace
      }

      const result = await generateItineraryAPI(payload)
      
      if (result.status === 'success') {
        setItineraryResult(result.itinerary, result.trip_id)
        toast.success('Your itinerary is ready!')
        navigate('/itinerary')
      } else {
        throw new Error(result.message || 'Failed to generate itinerary')
      }
    } catch (err) {
      console.error('Generation error:', err)
      const msg = err.response?.data?.detail || err.message || 'Something went wrong. Please try again.'
      setError(msg)
      toast.error(msg)
      setGenerating(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      {isGenerating && <LoadingScreen onCancel={() => setGenerating(false)} />}

      <div className="max-w-3xl mx-auto">
        {/* Progress Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">
            <span className={step >= 1 ? 'text-sky-600 font-bold' : ''}>1. Destination & Dates</span>
            <span className={step >= 2 ? 'text-sky-600 font-bold' : ''}>2. Budget & Companions</span>
            <span className={step >= 3 ? 'text-sky-600 font-bold' : ''}>3. Style & Preferences</span>
          </div>

          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div 
              className="bg-gradient-to-r from-sky-500 to-indigo-600 h-full transition-all duration-300 rounded-full"
              style={{ width: `${(step / 3) * 100}%` }}
            />
          </div>
        </div>

        {/* Card Container */}
        <div className="bg-white rounded-3xl p-6 sm:p-10 shadow-xl border border-slate-100">
          
          {/* ================= STEP 1: WHERE & WHEN ================= */}
          {step === 1 && (
            <div className="space-y-6 animate-in fade-in duration-200">
              <div>
                <h2 className="text-2xl font-extrabold text-slate-900">Where are you heading?</h2>
                <p className="text-sm text-slate-500 mt-1">Choose a destination and travel dates for your adventure.</p>
              </div>

              {/* Destination */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">
                  Destination City or Region
                </label>
                <div className="relative">
                  <MapPin className="w-5 h-5 absolute left-3.5 top-3.5 text-slate-400" />
                  <input
                    type="text"
                    value={formData.destination}
                    onChange={(e) => setFormField('destination', e.target.value)}
                    placeholder="e.g. Jaipur, Rajasthan or Paris, France"
                    className="w-full pl-11 pr-4 py-3 rounded-2xl border border-slate-200 focus:border-sky-500 focus:ring-4 focus:ring-sky-100 outline-none text-slate-800 font-medium transition"
                  />
                </div>
                {formErrors.destination && (
                  <p className="text-xs text-red-500 mt-1.5 flex items-center gap-1">
                    <AlertCircle className="w-3.5 h-3.5" /> {formErrors.destination}
                  </p>
                )}

                {/* Quick suggestions */}
                <div className="mt-3">
                  <span className="text-xs font-medium text-slate-400">Popular ideas:</span>
                  <div className="flex flex-wrap gap-1.5 mt-1.5">
                    {POPULAR_DESTINATIONS.slice(0, 5).map((dest) => (
                      <button
                        type="button"
                        key={dest}
                        onClick={() => setFormField('destination', dest)}
                        className="text-xs bg-slate-100 hover:bg-sky-50 hover:text-sky-700 text-slate-600 px-2.5 py-1 rounded-lg transition"
                      >
                        {dest}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Dates */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1.5">Start Date</label>
                  <div className="relative">
                    <Calendar className="w-5 h-5 absolute left-3.5 top-3.5 text-slate-400" />
                    <input
                      type="date"
                      value={formData.startDate}
                      onChange={(e) => setFormField('startDate', e.target.value)}
                      className="w-full pl-11 pr-4 py-3 rounded-2xl border border-slate-200 focus:border-sky-500 focus:ring-4 focus:ring-sky-100 outline-none text-slate-800 font-medium transition"
                    />
                  </div>
                  {formErrors.startDate && <p className="text-xs text-red-500 mt-1">{formErrors.startDate}</p>}
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1.5">End Date</label>
                  <div className="relative">
                    <Calendar className="w-5 h-5 absolute left-3.5 top-3.5 text-slate-400" />
                    <input
                      type="date"
                      value={formData.endDate}
                      onChange={(e) => setFormField('endDate', e.target.value)}
                      className="w-full pl-11 pr-4 py-3 rounded-2xl border border-slate-200 focus:border-sky-500 focus:ring-4 focus:ring-sky-100 outline-none text-slate-800 font-medium transition"
                    />
                  </div>
                  {formErrors.endDate && <p className="text-xs text-red-500 mt-1">{formErrors.endDate}</p>}
                </div>
              </div>

              {numDays > 0 && (
                <div className="p-3 bg-sky-50 border border-sky-100 rounded-xl text-sky-800 text-sm font-medium flex items-center justify-between">
                  <span>Trip Duration:</span>
                  <span className="font-bold">{numDays} {numDays === 1 ? 'Day' : 'Days'}</span>
                </div>
              )}
            </div>
          )}

          {/* ================= STEP 2: WHO & BUDGET ================= */}
          {step === 2 && (
            <div className="space-y-6 animate-in fade-in duration-200">
              <div>
                <h2 className="text-2xl font-extrabold text-slate-900">Budget & Companions</h2>
                <p className="text-sm text-slate-500 mt-1">Set your spending limit and tell us who is traveling.</p>
              </div>

              {/* Group Type */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Who is traveling?</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                  {[
                    { id: 'solo', label: 'Solo', icon: '🎒' },
                    { id: 'couple', label: 'Couple', icon: '👫' },
                    { id: 'family', label: 'Family', icon: '👨‍👩‍👧‍👦' },
                    { id: 'group', label: 'Friends Group', icon: '🎉' }
                  ].map((grp) => (
                    <button
                      type="button"
                      key={grp.id}
                      onClick={() => {
                        setFormField('groupType', grp.id)
                        if (grp.id === 'solo') setFormField('groupSize', 1)
                        if (grp.id === 'couple') setFormField('groupSize', 2)
                      }}
                      className={`py-3 px-3 rounded-2xl border text-center font-medium transition flex flex-col items-center gap-1 ${
                        formData.groupType === grp.id
                          ? 'border-sky-600 bg-sky-50 text-sky-900 ring-2 ring-sky-200'
                          : 'border-slate-200 hover:border-slate-300 text-slate-700'
                      }`}
                    >
                      <span className="text-2xl">{grp.icon}</span>
                      <span className="text-sm">{grp.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {formData.groupType === 'group' && (
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Group Size</label>
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={formData.groupSize}
                    onChange={(e) => setFormField('groupSize', e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-sky-500 outline-none"
                  />
                  {formErrors.groupSize && <p className="text-xs text-red-500 mt-1">{formErrors.groupSize}</p>}
                </div>
              )}

              {/* Total Budget & Currency */}
              <div>
                <div className="flex justify-between items-center mb-1.5">
                  <label className="text-sm font-semibold text-slate-700">Total Budget</label>
                  {numDays > 0 && (
                    <span className="text-xs font-semibold text-slate-500">
                      ~ {formData.currency} {perDayBudget} / day
                    </span>
                  )}
                </div>

                <div className="flex gap-2">
                  <select
                    value={formData.currency}
                    onChange={(e) => setFormField('currency', e.target.value)}
                    className="px-3.5 py-3 rounded-2xl border border-slate-200 font-semibold text-slate-700 bg-slate-50 outline-none"
                  >
                    <option value="INR">INR (₹)</option>
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                    <option value="GBP">GBP (£)</option>
                  </select>

                  <div className="relative flex-1">
                    <input
                      type="number"
                      step="500"
                      value={formData.budgetTotal}
                      onChange={(e) => setFormField('budgetTotal', e.target.value)}
                      placeholder="e.g. 20000"
                      className="w-full px-4 py-3 rounded-2xl border border-slate-200 focus:border-sky-500 focus:ring-4 focus:ring-sky-100 outline-none text-slate-900 font-bold text-lg"
                    />
                  </div>
                </div>
                {formErrors.budgetTotal && <p className="text-xs text-red-500 mt-1.5">{formErrors.budgetTotal}</p>}
              </div>

              {/* Accommodation Preference */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Accommodation Style</label>
                <select
                  value={formData.accommodationPreference}
                  onChange={(e) => setFormField('accommodationPreference', e.target.value)}
                  className="w-full px-4 py-3 rounded-2xl border border-slate-200 font-medium text-slate-700 bg-white outline-none focus:border-sky-500"
                >
                  <option value="hotel">Comfortable 3-4 Star Hotels</option>
                  <option value="budget_hostel">Hostels / Homestays (Budget)</option>
                  <option value="luxury_resort">Luxury 5-Star Resorts</option>
                  <option value="boutique">Boutique & Heritage Stays</option>
                </select>
              </div>
            </div>
          )}

          {/* ================= STEP 3: STYLE & INTERESTS ================= */}
          {step === 3 && (
            <div className="space-y-6 animate-in fade-in duration-200">
              <div>
                <h2 className="text-2xl font-extrabold text-slate-900">What’s your travel style?</h2>
                <p className="text-sm text-slate-500 mt-1">Personalize activities to match your vibe and hobbies.</p>
              </div>

              {/* Travel Style Grid */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Vibe & Pacing</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {TRAVEL_STYLES.map((style) => {
                    const Icon = style.icon
                    const isSelected = formData.travelStyle === style.id
                    return (
                      <div
                        key={style.id}
                        onClick={() => setFormField('travelStyle', style.id)}
                        className={`p-3.5 rounded-2xl border cursor-pointer transition flex items-start gap-3 ${
                          isSelected
                            ? 'border-sky-600 bg-sky-50 ring-2 ring-sky-200'
                            : 'border-slate-200 hover:border-slate-300'
                        }`}
                      >
                        <div className={`p-2 rounded-xl ${isSelected ? 'bg-sky-600 text-white' : 'bg-slate-100 text-slate-600'}`}>
                          <Icon className="w-5 h-5" />
                        </div>
                        <div>
                          <h4 className="text-sm font-bold text-slate-900">{style.label}</h4>
                          <p className="text-xs text-slate-500 mt-0.5">{style.desc}</p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* Pace */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Schedule Intensity</label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { id: 'slow', label: 'Slow & Leisurely', desc: '2-3 items/day' },
                    { id: 'moderate', label: 'Balanced', desc: '3-4 items/day' },
                    { id: 'fast', label: 'Packed & Fast', desc: '5-6 items/day' }
                  ].map((p) => (
                    <button
                      type="button"
                      key={p.id}
                      onClick={() => setFormField('pace', p.id)}
                      className={`py-2.5 px-2 rounded-xl border text-center transition ${
                        formData.pace === p.id 
                          ? 'border-indigo-600 bg-indigo-50 text-indigo-900 font-bold' 
                          : 'border-slate-200 text-slate-600 font-medium'
                      }`}
                    >
                      <div className="text-xs">{p.label}</div>
                      <div className="text-[10px] text-slate-400 mt-0.5">{p.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Interests Multi-Select */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Interests & Activities (Pick any)</label>
                <div className="flex flex-wrap gap-2">
                  {INTEREST_TAGS.map((tag) => {
                    const isSelected = formData.interests?.includes(tag)
                    return (
                      <button
                        type="button"
                        key={tag}
                        onClick={() => toggleInterest(tag)}
                        className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
                          isSelected
                            ? 'bg-sky-600 text-white shadow-sm shadow-sky-200'
                            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                        }`}
                      >
                        {isSelected ? '✓ ' : '+ '}{tag}
                      </button>
                    )
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="mt-8 pt-6 border-t border-slate-100 flex justify-between items-center">
            {step > 1 ? (
              <button
                type="button"
                onClick={handleBack}
                className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-100 transition"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </button>
            ) : <div />}

            {step < 3 ? (
              <button
                type="button"
                onClick={handleNext}
                className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl text-sm font-bold bg-sky-600 text-white hover:bg-sky-700 shadow-md shadow-sky-200 transition"
              >
                <span>Continue</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                onClick={handleGenerate}
                disabled={isGenerating}
                className="inline-flex items-center gap-2 px-7 py-3.5 rounded-2xl text-sm font-bold bg-gradient-to-r from-sky-600 to-indigo-600 text-white hover:from-sky-700 hover:to-indigo-700 shadow-lg shadow-sky-200 transition"
              >
                <Sparkles className="w-5 h-5 animate-pulse" />
                <span>Generate Itinerary 🚀</span>
              </button>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}
