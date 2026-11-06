import React, { useState } from 'react';
import { ThreeStageViewport } from './ThreeStageViewport';
import { Html5HybridViewport } from './Html5HybridViewport';
import { ManimSyncedViewport } from './ManimSyncedViewport';

type Theme = 'THEME_OBSIDIAN_DARK' | 'THEME_DAYLIGHT_PAPER' | 'THEME_DEEP_SPACE_COSMIC' | 'THEME_CYBER_GRID';
type ConceptArtStyle = 'DARK_MANHWA_ABYSS' | 'WESTERN_GRAPHIC_VECTOR' | 'RETRO_16BIT_GRID' | 'VOXEL_3D_CONSTRUCT' | 'HARD_SCIFI_TELEMETRY';
type ActiveEngine = 'THREE' | 'HTML5' | 'MANIM';

export const ModularStudioViewport: React.FC = () => {
    const [theme, setTheme] = useState<Theme>('THEME_OBSIDIAN_DARK');
    const [artStyle, setArtStyle] = useState<ConceptArtStyle>('VOXEL_3D_CONSTRUCT');
    const [activeEngine, setActiveEngine] = useState<ActiveEngine>('THREE');
    const [direction, setDirection] = useState<'ltr' | 'rtl'>('ltr');

    const getThemeStyles = () => {
        switch(theme) {
            case 'THEME_DAYLIGHT_PAPER': return 'bg-gray-50 text-gray-900';
            case 'THEME_DEEP_SPACE_COSMIC': return 'bg-[#0b0c10] text-purple-200';
            case 'THEME_CYBER_GRID': return 'bg-black text-green-400 bg-[linear-gradient(#002200_1px,transparent_1px),linear-gradient(90deg,#002200_1px,transparent_1px)] bg-[size:20px_20px]';
            case 'THEME_OBSIDIAN_DARK':
            default: return 'bg-gray-950 text-gray-100';
        }
    };

    return (
        <div className={`w-full min-h-screen flex flex-col transition-colors duration-500 ${getThemeStyles()}`} dir={direction}>
            {/* Top Navigation / Status */}
            <header className="h-14 border-b border-gray-700/50 flex items-center justify-between px-6 bg-black/20 backdrop-blur-sm z-50">
                <div className="font-bold text-lg tracking-wider">Multi-Engine Studio</div>
                <div className="flex space-x-4 text-sm items-center">
                    <select
                        value={direction}
                        onChange={(e) => setDirection(e.target.value as 'ltr'|'rtl')}
                        className="bg-transparent border border-gray-600 rounded px-2 py-1 text-inherit"
                    >
                        <option value="ltr">English (LTR)</option>
                        <option value="rtl">فارسی (RTL)</option>
                    </select>
                </div>
            </header>

            {/* Main Stage Area */}
            <main className="flex-1 p-6 flex items-center justify-center relative">
                <div className="w-full max-w-5xl h-[600px] shadow-2xl rounded-xl overflow-hidden ring-1 ring-white/10 relative">
                    {activeEngine === 'THREE' && <ThreeStageViewport />}
                    {activeEngine === 'HTML5' && <Html5HybridViewport />}
                    {activeEngine === 'MANIM' && <ManimSyncedViewport />}

                    {/* Live Concept-Art Deck Switcher (Floating) */}
                    <div className="absolute top-4 right-4 bg-black/80 backdrop-blur border border-gray-700 p-3 rounded-lg flex flex-col gap-2 z-40">
                        <span className="text-xs text-gray-400 uppercase tracking-wider font-bold mb-1">Renderer Engine</span>
                        <div className="flex gap-2 bg-gray-900 rounded p-1">
                            {(['THREE', 'HTML5', 'MANIM'] as ActiveEngine[]).map(engine => (
                                <button
                                    key={engine}
                                    onClick={() => setActiveEngine(engine)}
                                    className={`px-3 py-1 text-xs rounded transition-colors ${activeEngine === engine ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800'}`}
                                >
                                    {engine}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </main>

            {/* Chameleon Adaptive UI Bottom Drawer */}
            <footer className="border-t border-gray-700/50 bg-black/40 p-4 z-50">
                <div className="max-w-7xl mx-auto flex flex-wrap gap-6 items-end justify-between">
                    <div>
                        <label className="block text-xs uppercase tracking-wider text-gray-500 mb-2">Chameleon Theme</label>
                        <select
                            value={theme}
                            onChange={(e) => setTheme(e.target.value as Theme)}
                            className="bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white min-w-[200px]"
                        >
                            <option value="THEME_OBSIDIAN_DARK">Obsidian Dark</option>
                            <option value="THEME_DAYLIGHT_PAPER">Daylight Paper</option>
                            <option value="THEME_DEEP_SPACE_COSMIC">Deep Space</option>
                            <option value="THEME_CYBER_GRID">Cyber Grid</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-xs uppercase tracking-wider text-gray-500 mb-2">Concept-Art Paradigm (30%)</label>
                        <select
                            value={artStyle}
                            onChange={(e) => setArtStyle(e.target.value as ConceptArtStyle)}
                            className="bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white min-w-[200px]"
                        >
                            <option value="DARK_MANHWA_ABYSS">Dark Manhwa Abyss</option>
                            <option value="WESTERN_GRAPHIC_VECTOR">Western Graphic</option>
                            <option value="RETRO_16BIT_GRID">Retro 16-Bit</option>
                            <option value="VOXEL_3D_CONSTRUCT">Voxel 3D Construct</option>
                            <option value="HARD_SCIFI_TELEMETRY">Hard Sci-Fi Telemetry</option>
                        </select>
                    </div>

                    <div className="flex-1 flex justify-end">
                        <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 text-xs text-gray-400">
                            <strong>Engine Status:</strong> Local Ollama (qwen2.5:7b) Active | R2 Storage Online
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};
