export default function RecommendationPanel({ recommendations }: { recommendations: any[] }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="mt-4">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 flex items-center gap-2">
        <span>💡</span> Circular Economy Interventions
      </h2>
      <div className="grid grid-cols-1 gap-4">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow p-6 border-l-4 border-green-500 relative overflow-hidden">
            <div className="absolute top-0 right-0 bg-green-100 text-green-800 font-bold px-3 py-1 rounded-bl-lg text-sm">
              Rank {idx + 1}
            </div>
            <h3 className="text-lg font-bold text-gray-800 mb-2 pr-16">{rec.title}</h3>
            <p className="text-gray-600 mb-4">{rec.description}</p>
            
            <div className="grid grid-cols-2 gap-4 mb-4 bg-gray-50 p-3 rounded-lg">
              <div>
                <div className="text-xs text-gray-500 uppercase font-semibold">Est. CO₂ Reduction</div>
                <div className="text-green-600 font-bold">{rec.estimated_co2_reduction}</div>
              </div>
              <div>
                <div className="text-xs text-gray-500 uppercase font-semibold">Cost Impact</div>
                <div className="text-blue-600 font-bold">{rec.cost_impact}</div>
              </div>
            </div>
            
            <div className="mb-2">
              <span className="font-semibold text-gray-700">Why this works: </span>
              <span className="text-gray-600 text-sm">{rec.justification}</span>
            </div>
            
            <div>
              <span className="font-semibold text-gray-700">How to implement: </span>
              <span className="text-gray-600 text-sm">{rec.implementation_steps}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
