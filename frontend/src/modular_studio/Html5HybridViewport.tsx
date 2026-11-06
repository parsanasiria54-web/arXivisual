import React, { useState } from 'react';

export const Html5HybridViewport: React.FC = () => {
    const [bundleCount, setBundleCount] = useState(9);
    const [isBundled, setIsBundled] = useState(false);

    const handleSingleClickIgnition = () => {
        if (bundleCount === 9) {
            setBundleCount(10);
            setIsBundled(true);
        } else if (bundleCount === 10) {
            setBundleCount(0);
            setIsBundled(false);
        } else {
            setBundleCount(prev => prev + 1);
        }
    };

    return (
        <div className="html5-hybrid-viewport w-full h-full relative bg-gray-100 border border-gray-300 rounded-lg flex flex-col items-center justify-center p-4 overflow-hidden">
            <h2 className="text-gray-800 text-xl font-bold absolute top-4 left-4">2D Vector & Pixel Canvas</h2>

            <div className="flex-1 w-full flex items-center justify-center">
                {/* SVG Canvas for Crisp Vector / Pixel Art */}
                <svg width="400" height="300" className="bg-white shadow-lg border border-gray-200">
                    <rect x="10" y="10" width="380" height="280" fill="none" stroke="#ddd" strokeWidth="2" />

                    {/* Example of 10% Interaction - Single Click Ignition */}
                    <g
                        transform="translate(150, 100)"
                        onClick={handleSingleClickIgnition}
                        className="cursor-pointer hover:opacity-80 transition-opacity"
                    >
                        <circle cx="50" cy="50" r={isBundled ? "45" : "40"} fill={isBundled ? "#10b981" : "#3b82f6"} />
                        <text x="50" y="55" textAnchor="middle" fill="white" fontSize="20" fontWeight="bold">
                            {isBundled ? "Base-10 Bundle!" : bundleCount}
                        </text>
                    </g>

                    <text x="200" y="250" textAnchor="middle" fill="#666" fontSize="12">
                        Click the circle (Single-Click Ignition)
                    </text>
                </svg>
            </div>

            <div className="absolute bottom-4 right-4 bg-gray-800 text-white p-2 rounded text-xs shadow-md">
                10% Interaction: Effortless drag-drop & single click
            </div>
        </div>
    );
};
