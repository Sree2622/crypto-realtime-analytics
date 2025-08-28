import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

const API_BASE = process.env.REACT_APP_API_BASE || "/api";



export default function ChartView() {
  const [data, setData] = useState([]);
  const [symbol, setSymbol] = useState("bitcoin");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const interval = setInterval(fetchData, 3000);
    fetchData();
    return () => clearInterval(interval);
  }, [symbol]);

  async function fetchData() {
    try {
      setLoading(true);
      setError(null);
      const res = await axios.get(`${API_BASE}/aggregates?symbol=${symbol}`);
      const points = res.data
        .slice()
        .reverse()
        .map((r) => ({
          time: r.window_start.substring(11, 19) || r.window_start,
          avg: Number(r.avg_price),
        }));
      setData(points);
    } catch (e) {
      console.error("API fetch error", e);
      setError("Failed to load data. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-white shadow-xl rounded-2xl p-6 w-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Crypto Price Trends</h2>
        <select
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="border rounded-lg px-3 py-1 text-sm"
        >
          <option value="bitcoin">Bitcoin (BTC)</option>
          <option value="ethereum">Ethereum (ETH)</option>
        </select>
      </div>

      {loading && data.length === 0 ? (
        <p className="text-gray-500 text-center">Loading data...</p>
      ) : error ? (
        <p className="text-red-500 text-center">{error}</p>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="time" tick={{ fontSize: 12 }} />
            <YAxis domain={["auto", "auto"]} tick={{ fontSize: 12 }} />
            <Tooltip
              formatter={(value) =>
                `$${Number(value).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}`
              }
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="avg"
              name="Avg Price (USD)"
              stroke="#6366f1"
              strokeWidth={2}
              dot={false}
              isAnimationActive={true}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

