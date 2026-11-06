import React, { useState } from 'react';

export const ManimSyncedViewport: React.FC = () => {
    const [isPlaying, setIsPlaying] = useState(true);

    const togglePlayback = () => setIsPlaying(!isPlaying);

    return (
        <div className="manim-synced-viewport w-full h-full relative bg-black border border-gray-800 rounded-lg flex flex-col items-center justify-center p-4">
            <h2 className="text-white text-xl font-bold absolute top-4 left-4 z-10 drop-shadow-md">Manim Sync Player</h2>

            <div className="relative w-full max-w-3xl aspect-video bg-gray-900 border border-gray-700 flex items-center justify-center overflow-hidden">
                {/* Mock Video Element */}
                <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                    <div className="text-center">
                        <div className="text-4xl mb-4 font-serif text-white opacity-80">e^{`{i\\pi}`} + 1 = 0</div>
                        <span className="text-gray-400 text-sm">
                            [ Manim MP4 Render {isPlaying ? 'Playing...' : 'Paused'} ]
                        </span>
                    </div>
                </div>

                {/* 10% Interaction - Pause on micro-trigger overlay */}
                {!isPlaying && (
                    <div className="absolute inset-0 bg-black/60 flex items-center justify-center backdrop-blur-sm z-20">
                        <div className="bg-gray-800 p-6 rounded-lg shadow-xl max-w-md text-center border border-gray-700">
                            <h3 className="text-white font-bold text-lg mb-2">Micro-Trigger Opportunity</h3>
                            <p className="text-gray-300 text-sm mb-4">
                                The concept has paused to allow a zero-stress interaction.
                                Click below to step through the visualization.
                            </p>
                            <button
                                onClick={togglePlayback}
                                className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded w-full transition-colors"
                            >
                                Trigger Next Step
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* Playback Controls (Mock) */}
            <div className="mt-4 flex space-x-4 items-center bg-gray-800 p-2 rounded-full px-6">
                <button
                    onClick={togglePlayback}
                    className="w-10 h-10 rounded-full bg-white text-black flex items-center justify-center hover:bg-gray-200 transition-colors font-bold"
                >
                    {isPlaying ? '||' : '▶'}
                </button>
                <div className="w-64 h-2 bg-gray-600 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-500 w-1/3"></div>
                </div>
                <span className="text-xs text-gray-400">01:24 / 04:30</span>
            </div>
        </div>
    );
};
