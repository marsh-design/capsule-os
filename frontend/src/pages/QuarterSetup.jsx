import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function QuarterSetup() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    quarter: 'Q1',
    climate: 'moderate',
    style_keywords: [],
    budget: 1000,
    shopping_preferences: [],
  })
  const [loading, setLoading] = useState(false)

  const styleOptions = ['effortless', 'elevated', 'sexy', 'minimal', 'classic']
  const brandOptions = ['Everlane', 'Aritzia', 'Zara', 'Reformation', 'Madewell']

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/api/generate-capsule', formData)
      // Store capsule data (in real app, use state management)
      localStorage.setItem('capsule', JSON.stringify(response.data))
      navigate('/capsule')
    } catch (error) {
      console.error('Error generating capsule:', error)
      alert('Error generating capsule. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const toggleStyleKeyword = (keyword) => {
    setFormData(prev => ({
      ...prev,
      style_keywords: prev.style_keywords.includes(keyword)
        ? prev.style_keywords.filter(k => k !== keyword)
        : [...prev.style_keywords, keyword].slice(0, 3) // Max 3
    }))
  }

  const toggleBrand = (brand) => {
    setFormData(prev => ({
      ...prev,
      shopping_preferences: prev.shopping_preferences.includes(brand)
        ? prev.shopping_preferences.filter(b => b !== brand)
        : [...prev.shopping_preferences, brand]
    }))
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Quarter Setup</h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Quarter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quarter
          </label>
          <select
            value={formData.quarter}
            onChange={(e) => setFormData(prev => ({ ...prev, quarter: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="Q1">Q1 (Jan-Mar)</option>
            <option value="Q2">Q2 (Apr-Jun)</option>
            <option value="Q3">Q3 (Jul-Sep)</option>
            <option value="Q4">Q4 (Oct-Dec)</option>
          </select>
        </div>

        {/* Climate */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Climate
          </label>
          <select
            value={formData.climate}
            onChange={(e) => setFormData(prev => ({ ...prev, climate: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="cold">Cold</option>
            <option value="moderate">Moderate</option>
            <option value="warm">Warm</option>
            <option value="hot">Hot</option>
          </select>
        </div>

        {/* Style Keywords */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Style Keywords (select up to 3)
          </label>
          <div className="flex flex-wrap gap-2">
            {styleOptions.map(keyword => (
              <button
                key={keyword}
                type="button"
                onClick={() => toggleStyleKeyword(keyword)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  formData.style_keywords.includes(keyword)
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {keyword}
              </button>
            ))}
          </div>
        </div>

        {/* Budget */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Budget ($)
          </label>
          <input
            type="number"
            min="500"
            max="10000"
            step="100"
            value={formData.budget}
            onChange={(e) => setFormData(prev => ({ ...prev, budget: parseFloat(e.target.value) }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        {/* Shopping Preferences */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Where You Shop
          </label>
          <div className="flex flex-wrap gap-2">
            {brandOptions.map(brand => (
              <button
                key={brand}
                type="button"
                onClick={() => toggleBrand(brand)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  formData.shopping_preferences.includes(brand)
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {brand}
              </button>
            ))}
          </div>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={loading || formData.style_keywords.length === 0}
          className="w-full bg-primary-600 text-white py-3 px-4 rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Generating Capsule...' : 'Generate Capsule'}
        </button>
      </form>
    </div>
  )
}
