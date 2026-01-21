import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function CapsuleOutput() {
  const navigate = useNavigate()
  const [capsule, setCapsule] = useState(null)

  useEffect(() => {
    const stored = localStorage.getItem('capsule')
    if (stored) {
      setCapsule(JSON.parse(stored))
    } else {
      // If no capsule, redirect to setup
      navigate('/')
    }
  }, [navigate])

  if (!capsule) {
    return <div>Loading...</div>
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        Your {capsule.quarter} Capsule
      </h1>

      {/* Palette */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Color Palette</h2>
        <div className="flex gap-4">
          {capsule.palette.map((color, idx) => (
            <div
              key={idx}
              className="w-16 h-16 rounded-full border-2 border-gray-300"
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>
      </div>

      {/* Outfit Formulas */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Outfit Formulas</h2>
        <ul className="space-y-2">
          {capsule.outfit_formulas.map((formula, idx) => (
            <li key={idx} className="text-gray-700">• {formula}</li>
          ))}
        </ul>
      </div>

      {/* Capsule Items */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Capsule Items (12)</h2>
        <div className="space-y-6">
          {capsule.items.map((item, idx) => (
            <div key={idx} className="border-b pb-4 last:border-b-0">
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {item.category}: {item.item_name}
              </h3>
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div className="bg-gray-50 p-4 rounded">
                  <div className="text-sm font-medium text-gray-600 mb-1">Best Value</div>
                  <div className="font-semibold">{item.best_value.brand} - {item.best_value.name}</div>
                  <div className="text-primary-600">${item.best_value.price.toFixed(2)}</div>
                  <div className="text-sm text-gray-600 mt-1">{item.best_value.reason}</div>
                </div>
                <div className="bg-gray-50 p-4 rounded">
                  <div className="text-sm font-medium text-gray-600 mb-1">Best Quality</div>
                  <div className="font-semibold">{item.best_quality.brand} - {item.best_quality.name}</div>
                  <div className="text-primary-600">${item.best_quality.price.toFixed(2)}</div>
                  <div className="text-sm text-gray-600 mt-1">{item.best_quality.reason}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Do Not Buy */}
      {capsule.do_not_buy && capsule.do_not_buy.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-red-900 mb-4">Do Not Buy</h2>
          <ul className="space-y-2">
            {capsule.do_not_buy.map((item, idx) => (
              <li key={idx} className="text-red-700">• {item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
