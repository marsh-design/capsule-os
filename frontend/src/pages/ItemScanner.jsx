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

  const verdictStyle = (verdict) => {
    switch (verdict) {
      case "buy":
        return "border-black text-black"
      case "wait":
        return "border-amber-600 text-amber-800"
      case "skip":
        return "border-neutral-400 text-neutral-600"
      default:
        return "border-stone-200 text-neutral-600"
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="font-serif text-4xl md:text-5xl font-medium tracking-tight text-black mb-2">
        Should I buy this?
      </h1>
      <p className="text-neutral-500 text-sm tracking-wide uppercase mb-12">
        Get a verdict
      </p>

      <div className="border-t border-stone-200 pt-8">
        <div className="flex gap-0 border-b border-stone-200 mb-8">
          <button
            type="button"
            onClick={() => setInputType("link")}
            className={`px-0 py-3 mr-8 text-[11px] font-medium tracking-wide uppercase transition-colors ${
              inputType === "link"
                ? "text-black border-b-2 border-black -mb-px"
                : "text-neutral-500 hover:text-black"
            }`}
          >
            Product link
          </button>
          <button
            type="button"
            onClick={() => setInputType("manual")}
            className={`px-0 py-3 text-[11px] font-medium tracking-wide uppercase transition-colors ${
              inputType === "manual"
                ? "text-black border-b-2 border-black -mb-px"
                : "text-neutral-500 hover:text-black"
            }`}
          >
            Manual entry
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {inputType === "link" ? (
            <div>
              <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
                URL
              </label>
              <input
                type="url"
                value={formData.product_link}
                onChange={(e) =>
                  setFormData((prev) => ({ ...prev, product_link: e.target.value }))
                }
                placeholder="https://..."
                className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors placeholder:text-neutral-400"
                required
              />
            </div>
          ) : (
            <>
              <div>
                <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
                  Description
                </label>
                <textarea
                  value={formData.product_description}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      product_description: e.target.value,
                    }))
                  }
                  placeholder="Describe the product..."
                  rows={4}
                  className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors placeholder:text-neutral-400 resize-none"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
                    Price ($)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, price: e.target.value }))
                    }
                    className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-3">
                    Brand
                  </label>
                  <input
                    type="text"
                    value={formData.brand}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, brand: e.target.value }))
                    }
                    className="w-full bg-transparent border-b border-stone-300 py-3 text-black font-sans focus:border-black transition-colors"
                  />
                </div>
              </div>
            </>
          )}

          {error && (
            <p className="text-sm text-red-600 border-l-2 border-red-500 pl-4">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-black text-white py-4 text-xs font-medium tracking-wide uppercase hover:bg-neutral-800 disabled:opacity-40 disabled:cursor-not-allowed transition-opacity"
          >
            {loading ? (
              <span className="inline-flex items-center justify-center gap-2">
                <span className="inline-block h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Analyzing
              </span>
            ) : (
              "Analyze"
            )}
          </button>
        </form>
      </div>

      {analysis && (
        <div className="mt-16 space-y-12 border-t border-stone-200 pt-12">
          <div
            className={`border-l-2 pl-6 py-2 ${verdictStyle(analysis.verdict)}`}
          >
            <p className="text-[11px] font-medium tracking-wide uppercase opacity-70 mb-1">
              Verdict
            </p>
            <p className="font-serif text-3xl font-medium capitalize tracking-tight">
              {analysis.verdict}
            </p>
            <p className="text-sm mt-1 opacity-70">
              {(analysis.confidence * 100).toFixed(0)}% confidence
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            <div>
              <p className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-4">
                Pros
              </p>
              <ul className="space-y-2 text-sm text-black">
                {analysis.pros.map((pro, idx) => (
                  <li key={idx}>— {pro}</li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-4">
                Cons
              </p>
              <ul className="space-y-2 text-sm text-neutral-600">
                {analysis.cons.map((con, idx) => (
                  <li key={idx}>— {con}</li>
                ))}
              </ul>
            </div>
          </div>

          {analysis.cost_per_wear_estimate != null && (
            <div className="border-t border-stone-200 pt-8">
              <p className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-1">
                Cost per wear
              </p>
              <p className="font-serif text-2xl text-black">
                ${analysis.cost_per_wear_estimate.toFixed(2)}
              </p>
            </div>
          )}

          {analysis.closet_overlap_warning && (
            <p className="text-sm text-amber-800 border-l-2 border-amber-500 pl-4">
              {analysis.closet_overlap_warning}
            </p>
          )}

          {analysis.alternatives?.length > 0 && (
            <div className="border-t border-stone-200 pt-8">
              <p className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-4">
                Alternatives
              </p>
              <div className="space-y-4">
                {analysis.alternatives.map((alt, idx) => (
                  <div
                    key={idx}
                    className="flex justify-between items-baseline gap-4 border-b border-stone-100 pb-4 last:border-0"
                  >
                    <div>
                      <p className="font-medium text-black">
                        {alt.brand} — {alt.name}
                      </p>
                      {alt.reason && (
                        <p className="text-xs text-neutral-500 mt-0.5">
                          {alt.reason}
                        </p>
                      )}
                    </div>
                    {alt.price != null && (
                      <p className="text-black font-medium shrink-0">
                        ${Number(alt.price).toFixed(2)}
                      </p>
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
