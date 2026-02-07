import { useState } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import { API_BASE } from "../lib/api"

export default function QuarterSetup() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    quarter: "Q1",
    climate: "moderate",
    style_three_words: "",
    budget: 1000,
    shopping_preferences: [],
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const brandOptions = ["Everlane", "Aritzia", "Zara", "Reformation", "Madewell"]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    const threeWords = (formData.style_three_words || "").trim()
    if (!threeWords) {
      setError("Describe your vibe in 3 words (e.g. relaxed, minimal, French).")
      return
    }
    setLoading(true)
    try {
      const payload = {
        quarter: formData.quarter,
        climate: formData.climate,
        style_three_words: threeWords,
        budget: formData.budget,
        shopping_preferences: formData.shopping_preferences,
      }
      const response = await axios.post(
        `${API_BASE}/api/generate-capsule`,
        payload
      )
      localStorage.setItem("capsule", JSON.stringify(response.data))
      navigate("/capsule")
    } catch (err) {
      console.error("Error generating capsule:", err)
      setError(
        err.response?.data?.detail || "Could not generate capsule. Try again."
      )
    } finally {
      setLoading(false)
    }
  }

  const toggleBrand = (brand) => {
    setFormData((prev) => ({
      ...prev,
      shopping_preferences: prev.shopping_preferences.includes(brand)
        ? prev.shopping_preferences.filter((b) => b !== brand)
        : [...prev.shopping_preferences, brand],
    }))
  }

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="font-serif text-4xl md:text-5xl font-medium tracking-tight text-black mb-2">
        Quarter Setup
      </h1>
      <p className="text-neutral-500 text-sm tracking-wide uppercase mb-12">
        Define your capsule
      </p>

      <form onSubmit={handleSubmit} className="space-y-10">
        <div className="grid grid-cols-2 gap-6">
          <div>
            <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
              Quarter
            </label>
            <select
              value={formData.quarter}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, quarter: e.target.value }))
              }
              className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors"
            >
              <option value="Q1">Q1 — Jan to Mar</option>
              <option value="Q2">Q2 — Apr to Jun</option>
              <option value="Q3">Q3 — Jul to Sep</option>
              <option value="Q4">Q4 — Oct to Dec</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
              Climate
            </label>
            <select
              value={formData.climate}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, climate: e.target.value }))
              }
              className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors"
            >
              <option value="cold">Cold</option>
              <option value="moderate">Moderate</option>
              <option value="warm">Warm</option>
              <option value="hot">Hot</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
            Your vibe in 3 words
          </label>
          <p className="text-xs text-neutral-500 mb-2">
            Like Alison Bornstein: e.g. relaxed, minimal, French — we’ll refine these into specific style cues.
          </p>
          <input
            type="text"
            value={formData.style_three_words}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                style_three_words: e.target.value,
              }))
            }
            placeholder="e.g. relaxed, minimal, French"
            className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors placeholder:text-neutral-400"
          />
        </div>

        <div>
          <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
            Budget ($)
          </label>
          <input
            type="number"
            min="500"
            max="10000"
            step="100"
            value={formData.budget}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                budget: parseFloat(e.target.value) || 1000,
              }))
            }
            className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors"
          />
        </div>

        <div>
          <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-4">
            Where you shop
          </label>
          <div className="flex flex-wrap gap-2">
            {brandOptions.map((brand) => (
              <button
                key={brand}
                type="button"
                onClick={() => toggleBrand(brand)}
                className={`px-4 py-2 text-xs font-medium tracking-wide uppercase transition-colors ${
                  formData.shopping_preferences.includes(brand)
                    ? "bg-black text-white"
                    : "bg-stone-100 text-neutral-600 hover:bg-stone-200 hover:text-black"
                }`}
              >
                {brand}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <p className="text-sm text-red-600 border-l-2 border-red-500 pl-4">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading || !formData.style_three_words.trim()}
          className="w-full bg-black text-white py-4 text-xs font-medium tracking-wide uppercase hover:bg-neutral-800 disabled:opacity-40 disabled:cursor-not-allowed transition-opacity"
        >
          {loading ? (
            <span className="inline-flex items-center justify-center gap-2">
              <span className="inline-block h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Generating
            </span>
          ) : (
            "Generate capsule"
          )}
        </button>
      </form>
    </div>
  )
}
