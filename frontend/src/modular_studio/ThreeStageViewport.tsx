import React, { useState } from 'react';

type CameraPerspective = 'FIRST_PERSON_POV' | 'THIRD_PERSON_FOLLOW' | 'ISOMETRIC_DIORAMA' | 'ORBITAL_FREE_CAM';

export const ThreeStageViewport: React.FC = () => {
    const [perspective, setPerspective] = useState<CameraPerspective>('ISOMETRIC_DIORAMA');

    const handleCameraShift = () => {
        // Example single key pulse / button click shifting perspective
        const perspectives: CameraPerspective[] = [
            'FIRST_PERSON_POV', 'THIRD_PERSON_FOLLOW', 'ISOMETRIC_DIORAMA', 'ORBITAL_FREE_CAM'
        ];
        const nextIndex = (perspectives.indexOf(perspective) + 1) % perspectives.length;
        setPerspective(perspectives[nextIndex]);
    };

    return (
        <div className="three-stage-viewport w-full h-full relative bg-gray-900 border border-gray-700 rounded-lg flex flex-col items-center justify-center p-4">
            <h2 className="text-white text-xl font-bold absolute top-4 left-4">3D Stage</h2>
            <div className="absolute top-4 right-4 flex space-x-2">
                <span className="text-gray-400 text-sm">Perspective: {perspective}</span>
                <button
                    onClick={handleCameraShift}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-2 py-1 rounded text-xs"
                >
                    Shift Cam
                </button>
            </div>

            {/* Mock Canvas Container */}
            <div className="w-full max-w-2xl aspect-video bg-black flex items-center justify-center border border-gray-800 rounded">
                <span className="text-gray-600">[ WebGL / Three.js Canvas Placeholder - Render: {perspective} ]</span>
            </div>

            <div className="absolute bottom-4 left-4 text-gray-500 text-xs max-w-md">
                10% Interaction: Use single key pulse or click to trigger camera shifts or node expansions without reflex stress.
            </div>
        </div>
    );
};
