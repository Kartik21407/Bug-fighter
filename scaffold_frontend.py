import os

base_dir = r"c:\Users\Anuj\Desktop\HackOut\circular-carbon\frontend\src"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write_file("App.tsx", """
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
""")

write_file("components/ProcessInputForm.tsx", """
import { useState } from 'react';
import axios from 'axios';

export default function ProcessInputForm({ onResult, setLoading }: { onResult: any, setLoading: any }) {
  const [company, setCompany] = useState('Acme Manufacturing');
  const [industry, setIndustry] = useState('Steel');
  const [items, setItems] = useState([
    { category: 'ENERGY', itemName: 'Natural Gas', quantity: 15000, unit: 'kWh' },
    { category: 'MATERIAL', itemName: 'Steel', quantity: 500, unit: 'kg' },
    { category: 'WASTE', itemName: 'Industrial Waste', quantity: 200, unit: 'kg' }
  ]);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await axios.post('/api/emissions/analyze', {
        companyName: company,
        industryType: industry,
        items
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert('Error analyzing data.');
    }
    setLoading(false);
  };

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Process Data Input</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Company Name</label>
          <input className="mt-1 w-full p-2 border rounded-md" value={company} onChange={e=>setCompany(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Industry Type</label>
          <select className="mt-1 w-full p-2 border rounded-md" value={industry} onChange={e=>setIndustry(e.target.value)}>
            <option>Steel</option>
            <option>Cement</option>
            <option>Textile</option>
            <option>Food Processing</option>
          </select>
        </div>
        
        <div className="mt-4">
          <h3 className="text-md font-medium text-gray-700 mb-2">Process Inputs</h3>
          {items.map((item, idx) => (
            <div key={idx} className="flex gap-2 mb-2 items-center bg-gray-50 p-2 rounded border">
              <div className="flex-1">
                <div className="text-xs text-gray-500">{item.category}</div>
                <div className="font-medium text-sm">{item.itemName}</div>
              </div>
              <div className="w-24">
                <input type="number" className="w-full p-1 text-sm border rounded" value={item.quantity} onChange={e => {
                  const newItems = [...items];
                  newItems[idx].quantity = Number(e.target.value);
                  setItems(newItems);
                }} />
              </div>
              <div className="text-xs text-gray-500 w-12">{item.unit}</div>
            </div>
          ))}
        </div>
        
        <button type="submit" className="mt-4 w-full bg-green-600 text-white font-medium py-2 rounded-md hover:bg-green-700 transition">
          Analyze Emissions
        </button>
      </form>
    </div>
  );
}
""")

write_file("components/EmissionDashboard.tsx", """
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const COLORS = ['#ef4444', '#f97316', '#eab308', '#3b82f6', '#8b5cf6'];

export default function EmissionDashboard({ result }: { result: any }) {
  const data = result.breakdowns.map((b: any) => ({
    name: b.itemName,
    value: b.percentage
  }));

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-2 text-gray-800">Emission Breakdown</h2>
      <div className="text-3xl font-bold text-red-600 mb-6">
        {result.totalCo2e.toLocaleString()} <span className="text-lg text-gray-500 font-normal">kg CO₂e Total</span>
      </div>
      
      <div className="flex flex-col md:flex-row items-center gap-8">
        <div className="w-full md:w-1/2 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={data} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                {data.map((_: any, index: number) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
              </Pie>
              <Tooltip formatter={(val: number) => val.toFixed(1) + '%'} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="w-full md:w-1/2">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-100 text-gray-600">
              <tr>
                <th className="p-2 rounded-tl">Source</th>
                <th className="p-2 text-right">kg CO₂e</th>
                <th className="p-2 text-right rounded-tr">%</th>
              </tr>
            </thead>
            <tbody>
              {result.breakdowns.map((b: any, idx: number) => (
                <tr key={idx} className="border-b last:border-0">
                  <td className="p-2 font-medium">{b.itemName}</td>
                  <td className="p-2 text-right text-gray-600">{b.co2e.toLocaleString(undefined, {maximumFractionDigits:0})}</td>
                  <td className="p-2 text-right text-red-500 font-medium">{b.percentage.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
""")

write_file("components/RecommendationPanel.tsx", """
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
""")

print("React frontend generated.")
