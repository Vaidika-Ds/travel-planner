import axios from 'axios'
import { supabase } from './supabase'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 90000, // 90 seconds to allow AI generation
})

// Request interceptor: attach Supabase JWT token automatically
api.interceptors.request.use(async (config) => {
  try {
    const { data: { session } } = await supabase.auth.getSession()
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`
    }
  } catch (error) {
    console.error('Error fetching Supabase session token:', error)
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export const generateItineraryAPI = async (payload) => {
  const response = await api.post('/itinerary/generate', payload)
  return response.data
}

export const fetchUserTripsAPI = async () => {
  const response = await api.get('/trips/')
  return response.data
}

export const fetchTripDetailsAPI = async (tripId) => {
  const response = await api.get(`/trips/${tripId}`)
  return response.data
}


export const regenerateDayAPI = async (payload) => {
  const response = await api.post('/itinerary/regenerate-day', payload)
  return response.data
}
