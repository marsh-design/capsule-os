import { useState } from "react"
import axios from "axios"
import { API_BASE } from "../lib/api"

export default function ItemScanner() {
  const [inputType, setInputType] = useState("link")
  const [formData, setFormData] = useState({
    product_link: "",
    product_description: "",
    price: "",
    brand: "",
  })
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const payload =
        inputType === "link"
          ? { product_link: formData.product_link }
          : {
              product_description: formData.product_description,
              price: formData.price ? parseFloat(formData.price) : null,
              brand: formData.brand,
            }

      const response = await axios.post(
        `${API_BASE}/api/analyze-item`,
        payload
      )
      setAnalysis(response.data)
    } catch (err) {
      console.error("Error analyzing item:", err)
      setError(
        err.response?.data?.detail || "Could not analyze item. Try again."
      )
    } finally {
      setLoading(false)
    }
  }

  const getVerdictColor = (verdict) => {
    switch (verdict) {
      case 'buy':
        return 'bg-green-100 text-green-800 border-green-300'
      case 'wait':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'skip':
        return 'bg-red-100 text-red-800 border-red-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getVerdictIcon = (verdict) => {
    switch (verdict) {
      case 'buy':
        return '✅'
      case 'wait':
        return '⚠️'
      case 'skip':
        return '❌'
      default:
        return '❓'
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Should I Buy This?</h1>

      {/* Input Type Toggle */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex gap-4 mb-4">
          <button
            onClick={() => setInputType('link')}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              inputType === 'link'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Product Link
          </button>
          <button
            onClick={() => setInputType('manual')}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              inputType === 'manual'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Manual Entry
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {inputType === 'link' ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Product URL
              </label>
              <input
                type="url"
                value={formData.product_link}
                onChange={(e) => setFormData(prev => ({ ...prev, product_link: e.target.value }))}
                placeholder="https://example.com/product"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                required
              />
            </div>
          ) : (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Product Description
                </label>
                <textarea
                  value={formData.product_description}
                  onChange={(e) => setFormData(prev => ({ ...prev, product_description: e.target.value }))}
                  placeholder="Describe the product..."
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Price ($)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={(e) => setFormData(prev => ({ ...prev, price: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Brand
                  </label>
                  <input
                    type="text"
                    value={formData.brand}
                    onChange={(e) => setFormData(prev => ({ ...prev, brand: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>
            </>
          )}

          {error && (
            <div className="rounded-md bg-red-50 border border-red-200 px-4 py-3 text-red-700 text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 text-white py-3 px-4 rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="inline-flex items-center gap-2">
                <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Analyzing...
              </span>
            ) : (
              "Analyze Item"
            )}
          </button>
        </form>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          {/* Verdict */}
          <div className={`border-2 rounded-lg p-6 ${getVerdictColor(analysis.verdict)}`}>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-3xl">{getVerdictIcon(analysis.verdict)}</span>
              <div>
                <h2 className="text-2xl font-bold capitalize">{analysis.verdict}</h2>
                <p className="text-sm opacity-75">Confidence: {(analysis.confidence * 100).toFixed(0)}%</p>
              </div>
            </div>
          </div>

          {/* Pros & Cons */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h3 className="text-lg font-semibold text-green-700 mb-2">Pros</h3>
              <ul className="space-y-1">
                {analysis.pros.map((pro, idx) => (
                  <li key={idx} className="text-gray-700">✓ {pro}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-red-700 mb-2">Cons</h3>
              <ul className="space-y-1">
                {analysis.cons.map((con, idx) => (
                  <li key={idx} className="text-gray-700">✗ {con}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Closet Overlap Warning */}
          {analysis.closet_overlap_warning && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-yellow-800">⚠️ {analysis.closet_overlap_warning}</p>
            </div>
          )}

          {/* Cost Per Wear */}
          {analysis.cost_per_wear_estimate && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-blue-800">
                <strong>Estimated Cost Per Wear:</strong> ${analysis.cost_per_wear_estimate.toFixed(2)}
              </p>
            </div>
          )}

          {/* Alternatives */}
          {analysis.alternatives && analysis.alternatives.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-3">Alternatives</h3>
              <div className="space-y-3">
                {analysis.alternatives.map((alt, idx) => (
                  <div key={idx} className="bg-gray-50 p-4 rounded-lg">
                    <div className="font-semibold">{alt.brand} - {alt.name}</div>
                    <div className="text-primary-600">
                      {alt.price != null ? `$${Number(alt.price).toFixed(2)}` : alt.reason || ""}
                    </div>
                    {alt.reason && alt.price != null && (
                      <div className="text-sm text-gray-600 mt-1">{alt.reason}</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
