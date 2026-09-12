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
              <Tooltip formatter={(val: any) => `${Number(val || 0).toFixed(1)}%`} />
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
