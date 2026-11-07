export default function ModularStudio() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-4">Modular Studio</h1>
      <p className="text-lg">Welcome to the Grand Unification Orchestrator (Phase 06).</p>

      <div className="mt-8 p-6 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-2xl font-semibold mb-4">Pipeline Status</h2>
        <p className="mb-2">Enter an arXiv ID or Topic below to begin.</p>

        <div className="flex space-x-4">
          <input
            type="text"
            placeholder="e.g., 2401.00123 or 'Dijkstra'"
            className="px-4 py-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-white w-64"
          />
          <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-md font-semibold transition">
            Launch
          </button>
        </div>
      </div>
    </div>
  );
}
