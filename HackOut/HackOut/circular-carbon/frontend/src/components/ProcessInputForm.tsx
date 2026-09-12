import { useState, useEffect } from 'react';
import axios from 'axios';

interface ProcessItem {
  category: string;
  itemName: string;
  quantity: number;
  unit: string;
}

const AVAILABLE_FACTORS: ProcessItem[] = [
  { category: 'ENERGY', itemName: 'Natural Gas', unit: 'kWh', quantity: 5000 },
  { category: 'ENERGY', itemName: 'Grid Electricity', unit: 'kWh', quantity: 8000 },
  { category: 'ENERGY', itemName: 'Coal', unit: 'kg', quantity: 3000 },
  { category: 'MATERIAL', itemName: 'Steel', unit: 'kg', quantity: 1500 },
  { category: 'MATERIAL', itemName: 'Aluminum', unit: 'kg', quantity: 500 },
  { category: 'MATERIAL', itemName: 'Cement', unit: 'kg', quantity: 4000 },
  { category: 'WASTE', itemName: 'Industrial Waste', unit: 'kg', quantity: 500 },
  { category: 'WASTE', itemName: 'Plastic Waste', unit: 'kg', quantity: 300 },
  { category: 'TRANSPORT', itemName: 'Diesel Truck', unit: 'liter', quantity: 600 }
];

const INDUSTRY_PRESETS: Record<string, { company: string; items: ProcessItem[] }> = {
  'Steel': {
    company: 'Apex Steel & Foundry Ltd',
    items: [
      { category: 'MATERIAL', itemName: 'Steel', quantity: 2500, unit: 'kg' },
      { category: 'ENERGY', itemName: 'Coal', quantity: 3500, unit: 'kg' },
      { category: 'ENERGY', itemName: 'Grid Electricity', quantity: 7000, unit: 'kWh' },
      { category: 'WASTE', itemName: 'Industrial Waste', quantity: 600, unit: 'kg' }
    ]
  },
  'Cement': {
    company: 'UltraBuild Cement Corp',
    items: [
      { category: 'MATERIAL', itemName: 'Cement', quantity: 6000, unit: 'kg' },
      { category: 'ENERGY', itemName: 'Coal', quantity: 4500, unit: 'kg' },
      { category: 'TRANSPORT', itemName: 'Diesel Truck', quantity: 800, unit: 'liter' },
      { category: 'WASTE', itemName: 'Industrial Waste', quantity: 700, unit: 'kg' }
    ]
  },
  'Food Processing': {
    company: 'FreshHarvest Foods Ltd',
    items: [
      { category: 'ENERGY', itemName: 'Natural Gas', quantity: 6000, unit: 'kWh' },
      { category: 'ENERGY', itemName: 'Grid Electricity', quantity: 9000, unit: 'kWh' },
      { category: 'WASTE', itemName: 'Plastic Waste', quantity: 450, unit: 'kg' },
      { category: 'TRANSPORT', itemName: 'Diesel Truck', quantity: 500, unit: 'liter' }
    ]
  },
  'Textile': {
    company: 'EcoWeave Textiles',
    items: [
      { category: 'ENERGY', itemName: 'Grid Electricity', quantity: 12000, unit: 'kWh' },
      { category: 'ENERGY', itemName: 'Natural Gas', quantity: 4000, unit: 'kWh' },
      { category: 'WASTE', itemName: 'Plastic Waste', quantity: 350, unit: 'kg' },
      { category: 'TRANSPORT', itemName: 'Diesel Truck', quantity: 300, unit: 'liter' }
    ]
  },
  'Chemical': {
    company: 'Synthex Chemical Solutions',
    items: [
      { category: 'ENERGY', itemName: 'Natural Gas', quantity: 8000, unit: 'kWh' },
      { category: 'MATERIAL', itemName: 'Aluminum', quantity: 600, unit: 'kg' },
      { category: 'WASTE', itemName: 'Industrial Waste', quantity: 1200, unit: 'kg' },
      { category: 'TRANSPORT', itemName: 'Diesel Truck', quantity: 600, unit: 'liter' }
    ]
  }
};

const CATEGORY_STYLES: Record<string, { bg: string; text: string }> = {
  ENERGY: { bg: 'bg-amber-100', text: 'text-amber-800' },
  MATERIAL: { bg: 'bg-blue-100', text: 'text-blue-800' },
  WASTE: { bg: 'bg-rose-100', text: 'text-rose-800' },
  TRANSPORT: { bg: 'bg-purple-100', text: 'text-purple-800' }
};

export default function ProcessInputForm({ onResult, setLoading }: { onResult: any; setLoading: any }) {
  const [industry, setIndustry] = useState('Steel');
  const [company, setCompany] = useState(INDUSTRY_PRESETS['Steel'].company);
  const [items, setItems] = useState<ProcessItem[]>(INDUSTRY_PRESETS['Steel'].items);
  const [showAddMenu, setShowAddMenu] = useState(false);

  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '';

  const triggerAnalyze = async (companyName: string, industryType: string, currentItems: ProcessItem[]) => {
    setLoading(true);
    try {
      const res = await axios.post(`${apiBaseUrl}/api/emissions/analyze`, {
        companyName,
        industryType,
        items: currentItems
      });
      onResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Auto-analyze on initial mount
  useEffect(() => {
    triggerAnalyze(company, industry, items);
  }, []);

  const handleIndustryChange = (newIndustry: string) => {
    setIndustry(newIndustry);
    const preset = INDUSTRY_PRESETS[newIndustry];
    if (preset) {
      setCompany(preset.company);
      setItems(preset.items);
      triggerAnalyze(preset.company, newIndustry, preset.items);
    }
  };

  const handleQuantityChange = (idx: number, qty: number) => {
    const newItems = [...items];
    newItems[idx].quantity = qty;
    setItems(newItems);
  };

  const handleAddItem = (factor: ProcessItem) => {
    // If factor already exists, don't duplicate, just focus
    if (!items.some(i => i.itemName === factor.itemName)) {
      setItems([...items, { ...factor }]);
    }
    setShowAddMenu(false);
  };

  const handleRemoveItem = (idx: number) => {
    if (items.length <= 1) return;
    setItems(items.filter((_, i) => i !== idx));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    triggerAnalyze(company, industry, items);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Process Data Input</h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1">
            Company Name
          </label>
          <input
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-900 focus:ring-2 focus:ring-green-500 focus:outline-none"
            value={company}
            onChange={e => setCompany(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1">
            Industry Type
          </label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-900 bg-white focus:ring-2 focus:ring-green-500 focus:outline-none cursor-pointer"
            value={industry}
            onChange={e => handleIndustryChange(e.target.value)}
          >
            {Object.keys(INDUSTRY_PRESETS).map(ind => (
              <option key={ind} value={ind}>{ind}</option>
            ))}
          </select>
        </div>

        <div className="mt-2">
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Process Inputs
            </label>
            <div className="relative">
              <button
                type="button"
                onClick={() => setShowAddMenu(!showAddMenu)}
                className="text-xs text-green-700 hover:text-green-800 font-medium flex items-center gap-1 hover:underline cursor-pointer"
              >
                + Add Input
              </button>
              {showAddMenu && (
                <div className="absolute right-0 top-6 z-20 w-56 bg-white border border-gray-200 rounded-lg shadow-xl py-1">
                  <div className="px-3 py-1.5 text-xs font-bold text-gray-400 uppercase tracking-wider border-b">
                    Available Factors
                  </div>
                  <div className="max-h-56 overflow-y-auto">
                    {AVAILABLE_FACTORS.map(factor => (
                      <button
                        key={factor.itemName}
                        type="button"
                        onClick={() => handleAddItem(factor)}
                        className="w-full text-left px-3 py-1.5 text-xs text-gray-700 hover:bg-green-50 hover:text-green-700 flex justify-between items-center cursor-pointer"
                      >
                        <span>{factor.itemName}</span>
                        <span className="text-[10px] text-gray-400 font-medium">[{factor.category}]</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="flex flex-col gap-2.5">
            {items.map((item, idx) => {
              const style = CATEGORY_STYLES[item.category] || { bg: 'bg-gray-100', text: 'text-gray-700' };
              return (
                <div
                  key={idx}
                  className="flex items-center justify-between p-3 rounded-lg border border-gray-200 bg-gray-50/70 hover:bg-white hover:border-gray-300 transition shadow-xs"
                >
                  <div className="flex flex-col gap-1 pr-2 flex-1">
                    <span className={`inline-block w-fit px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${style.bg} ${style.text}`}>
                      {item.category}
                    </span>
                    <span className="font-semibold text-sm text-gray-800">
                      {item.itemName}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min="0"
                      step="any"
                      className="w-24 px-2 py-1.5 text-right font-medium text-sm bg-white border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:outline-none"
                      value={item.quantity}
                      onChange={e => handleQuantityChange(idx, Number(e.target.value))}
                      required
                    />
                    <span className="text-xs font-medium text-gray-500 w-9 text-left">
                      {item.unit}
                    </span>
                    {items.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveItem(idx)}
                        className="text-gray-400 hover:text-red-500 text-sm transition px-1 cursor-pointer"
                        title="Remove input"
                      >
                        ✕
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <button
          type="submit"
          className="mt-2 w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2.5 rounded-lg transition duration-150 shadow-md flex items-center justify-center gap-2 cursor-pointer"
        >
          <span>⚡</span> Analyze Emissions
        </button>
      </form>
    </div>
  );
}
