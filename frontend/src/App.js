import React from "react";
import ChartView from "./components/ChartView";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-6">📊 Real-time Crypto Dashboard</h1>
      <div className="w-full max-w-5xl">
        <ChartView />
      </div>
    </div>
  );
}

export default App;

