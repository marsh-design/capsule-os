import { useEffect, useState } from "react"
import { API_BASE } from "../lib/api"

const CATEGORIES = [
  "All",
  "Top",
  "Bottom",
  "Outerwear",
  "Shoes",
  "Dress",
  "Accessory",
]

export default function Browse() {
  const [products, setProducts] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState("All")

  useEffect(() => {
    const params = new URLSearchParams()
    if (category && category !== "All") params.set("category", category)
    fetch(`${API_BASE}/api/products?${params}`)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.products || [])
        setTotal(data.total ?? 0)
      })
      .catch(() => setProducts([]))
      .finally(() => setLoading(false))
  }, [category])

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-12">
        <p className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-2">
          Browse to plan
        </p>
        <h1 className="font-serif text-4xl md:text-5xl font-medium tracking-tight text-black">
          Catalog
        </h1>
      </header>

      <div className="flex flex-wrap gap-2 mb-8">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            type="button"
            onClick={() => setCategory(cat)}
            className={`text-[11px] font-medium tracking-wide uppercase px-4 py-2 border transition-colors ${
              category === cat
                ? "border-black bg-black text-white"
                : "border-stone-200 text-neutral-600 hover:border-black hover:text-black"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-24">
          <span className="inline-block h-6 w-6 animate-spin rounded-full border-2 border-black border-t-transparent" />
        </div>
      ) : products.length === 0 ? (
        <p className="text-neutral-500 text-sm">
          No products. Seed the database with <code className="bg-stone-100 px-1">python scripts/seed_db.py</code> in the backend.
        </p>
      ) : (
        <>
          <p className="text-[11px] text-neutral-500 mb-6 uppercase tracking-wide">
            {total} item{total !== 1 ? "s" : ""}
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 md:gap-8">
            {products.map((p) => (
              <article
                key={p.id}
                className="group border-t border-stone-200 pt-4"
              >
                <div className="block mb-3 aspect-[3/4] bg-stone-100 overflow-hidden">
                  {p.image_url ? (
                    <img
                      src={p.image_url}
                      alt={p.name}
                      className="w-full h-full object-cover group-hover:opacity-95 transition-opacity"
                      onError={(e) => {
                        e.target.style.display = "none"
                        e.target.nextElementSibling?.classList.remove("hidden")
                      }}
                    />
                  ) : null}
                  <div
                    className={`w-full h-full flex items-center justify-center text-neutral-400 text-sm uppercase tracking-wide ${
                      p.image_url ? "hidden" : ""
                    }`}
                  >
                    No image
                  </div>
                </div>
                <p className="text-[11px] uppercase tracking-wide text-neutral-500">
                  {p.category}
                </p>
                <p className="font-sans text-sm font-medium text-black mt-0.5">
                  {p.brand}
                </p>
                <p className="text-sm text-neutral-600 line-clamp-2">
                  {p.name}
                </p>
                <p className="mt-2 text-black font-medium">
                  ${Number(p.price).toFixed(2)}
                </p>
                {p.link && (
                  <a
                    href={p.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block mt-3 text-[11px] font-medium tracking-wide uppercase text-neutral-500 hover:text-black border-b border-transparent hover:border-black transition-colors"
                  >
                    View at {p.brand} →
                  </a>
                )}
              </article>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
