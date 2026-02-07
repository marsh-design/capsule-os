import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { getColorHex } from "../lib/colors"

export default function CapsuleOutput() {
  const [capsule, setCapsule] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const stored = localStorage.getItem("capsule")
    if (stored) {
      try {
        setCapsule(JSON.parse(stored))
      } catch {
        setCapsule(null)
      }
    } else {
      setCapsule(null)
    }
    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <span className="inline-block h-6 w-6 animate-spin rounded-full border-2 border-black border-t-transparent" />
      </div>
    )
  }

  if (!capsule) {
    return (
      <div className="max-w-md mx-auto text-center py-24">
        <h2 className="font-serif text-3xl font-medium tracking-tight text-black mb-3">
          No capsule yet
        </h2>
        <p className="text-neutral-500 text-sm tracking-wide uppercase mb-8">
          Create your first quarterly capsule to see your palette and items here.
        </p>
        <Link
          to="/"
          className="inline-block bg-black text-white px-8 py-4 text-xs font-medium tracking-wide uppercase hover:bg-neutral-800 transition-opacity"
        >
          Create capsule
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-16">
        <p className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-2">
          Your capsule
        </p>
        <h1 className="font-serif text-4xl md:text-5xl font-medium tracking-tight text-black">
          {capsule.quarter}
        </h1>
      </header>

      {/* Palette */}
      <section className="mb-20">
        <h2 className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-6">
          Palette
        </h2>
        <div className="flex flex-wrap gap-6">
          {capsule.palette.map((color, idx) => (
            <div key={idx} className="flex flex-col items-center">
              <div
                className="w-14 h-14 rounded-full border border-stone-200"
                style={{ backgroundColor: getColorHex(color) }}
                title={color}
              />
              <span className="text-[11px] text-neutral-500 mt-3 uppercase tracking-wide">
                {color}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Outfit formulas */}
      <section className="mb-20">
        <h2 className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-6">
          Outfit formulas
        </h2>
        <ul className="space-y-2">
          {capsule.outfit_formulas.map((formula, idx) => (
            <li
              key={idx}
              className="font-serif text-xl md:text-2xl text-black tracking-tight"
            >
              {formula}
            </li>
          ))}
        </ul>
      </section>

      {/* Capsule items — grid */}
      <section>
        <h2 className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-8">
          {capsule.items.length} items
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-10">
          {capsule.items.map((item, idx) => {
            const valueImg = item.best_value?.image_url
            const qualityImg = item.best_quality?.image_url
            const mainImg = valueImg || qualityImg
            return (
              <article
                key={idx}
                className="border-t border-stone-200 pt-6 group"
              >
                {mainImg && (
                  <div className="aspect-[3/4] w-full mb-6 bg-stone-100 overflow-hidden">
                    <img
                      src={mainImg}
                      alt={item.item_name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}
                <div className="flex items-start justify-between gap-4 mb-4">
                  <h3 className="font-serif text-2xl font-medium tracking-tight text-black">
                    {item.item_name}
                  </h3>
                  {item.palette_colors?.length > 0 && (
                    <div className="flex gap-1.5 shrink-0">
                      {item.palette_colors.map((color, cIdx) => (
                        <div
                          key={cIdx}
                          className="w-4 h-4 rounded-full border border-stone-200"
                          style={{ backgroundColor: getColorHex(color) }}
                          title={color}
                        />
                      ))}
                    </div>
                  )}
                </div>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <p className="text-[11px] uppercase tracking-wide text-neutral-500 mb-1">
                      Value
                    </p>
                    <p className="font-sans text-sm font-medium text-black">
                      {item.best_value.brand}
                    </p>
                    <p className="text-sm text-neutral-600">
                      {item.best_value.name}
                    </p>
                    <p className="mt-2 text-black font-medium">
                      ${item.best_value.price.toFixed(2)}
                    </p>
                    {item.best_value?.link && (
                      <a
                        href={item.best_value.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block mt-2 text-[11px] font-medium tracking-wide uppercase text-neutral-500 hover:text-black"
                      >
                        View at {item.best_value.brand} →
                      </a>
                    )}
                  </div>
                  <div>
                    <p className="text-[11px] uppercase tracking-wide text-neutral-500 mb-1">
                      Quality
                    </p>
                    <p className="font-sans text-sm font-medium text-black">
                      {item.best_quality.brand}
                    </p>
                    <p className="text-sm text-neutral-600">
                      {item.best_quality.name}
                    </p>
                    <p className="mt-2 text-black font-medium">
                      ${item.best_quality.price.toFixed(2)}
                    </p>
                    {item.best_quality?.link && (
                      <a
                        href={item.best_quality.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block mt-2 text-[11px] font-medium tracking-wide uppercase text-neutral-500 hover:text-black"
                      >
                        View at {item.best_quality.brand} →
                      </a>
                    )}
                  </div>
                </div>
              </article>
            )
          })}
        </div>
      </section>

      {capsule.do_not_buy?.length > 0 && (
        <section className="mt-20 pt-10 border-t border-stone-200">
          <h2 className="text-[11px] font-medium tracking-wide uppercase text-neutral-500 mb-4">
            Do not buy
          </h2>
          <ul className="space-y-1 text-sm text-neutral-600">
            {capsule.do_not_buy.map((item, idx) => (
              <li key={idx}>— {item}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
