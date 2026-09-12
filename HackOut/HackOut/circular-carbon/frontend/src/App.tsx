import { useState } from 'react';
import ProcessInputForm from './components/ProcessInputForm';
import EmissionDashboard from './components/EmissionDashboard';
import RecommendationPanel from './components/RecommendationPanel';

function App() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      <nav className="bg-green-700 text-white p-4 shadow-lg sticky top-0 z-10">
        <div className="max-w-7xl mx-auto flex items-center gap-3">
          <span className="text-2xl">♻️</span>
          <h1 className="text-xl font-bold">Circular Carbon</h1>
          <span className="text-sm text-green-200 ml-2 hidden sm:inline">Industrial Emission Leak-Point Detector</span>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto p-4 sm:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-4">
          <ProcessInputForm onResult={setResult} setLoading={setLoading} />
        </div>
        <div className="lg:col-span-8 flex flex-col gap-6">
          {loading && (
            <div className="bg-white rounded-xl shadow p-8 text-center animate-pulse">
              <div className="text-xl font-semibold text-green-600 mb-2">Analyzing process data...</div>
              <p className="text-gray-500">Calculating emissions and generating circular interventions.</p>
            </div>
          )}
          {!loading && result && (
            <>
              <EmissionDashboard result={result} />
              <RecommendationPanel recommendations={result.recommendations || []} />
            </>
          )}
          {!loading && !result && (
            <div className="bg-white rounded-xl shadow p-8 text-center h-full flex flex-col items-center justify-center text-gray-400">
              <span className="text-4xl mb-4">🏭</span>
              <p>Enter your process data to see emission breakdown and circular economy recommendations.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
export default App;
