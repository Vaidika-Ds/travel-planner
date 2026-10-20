import { create } from 'zustand'

export const useTripStore = create((set) => ({
  formData: {
    destination: '',
    startDate: '',
    endDate: '',
    budgetTotal: 15000,
    currency: 'INR',
    travelStyle: 'relaxed',
    interests: ['sightseeing', 'food'],
    groupType: 'solo',
    groupSize: 1,
    accommodationPreference: 'hotel',
    pace: 'moderate'
  },
  currentTrip: null,
  currentItinerary: null,
  isGenerating: false,
  error: null,

  setFormField: (field, value) => set((state) => ({
    formData: { ...state.formData, [field]: value }
  })),

  setFullFormData: (data) => set({ formData: data }),

  setGenerating: (isGenerating) => set({ isGenerating }),

  setItineraryResult: (itinerary, tripId) => set({
    currentItinerary: itinerary,
    currentTrip: tripId,
    isGenerating: false,
    error: null
  }),

  setError: (error) => set({ error, isGenerating: false }),

  resetTrip: () => set({
    currentTrip: null,
    currentItinerary: null,
    isGenerating: false,
    error: null
  })
}))
