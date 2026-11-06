from backend.core_ingestion.interfaces import ConceptDependencyDAG, MicroSceneScript, AVStimulusDirective, WorkingMemoryAnchor
from backend.core_ingestion.cognitive_decomposer import CognitiveDecomposer
from typing import List

class NarrativeWeaver:
    def __init__(self, decomposer: CognitiveDecomposer):
        self.decomposer = decomposer

    def weave(self, dag: ConceptDependencyDAG) -> List[MicroSceneScript]:
        sorted_nodes = self.decomposer.topological_sort(dag)

        scenes = []
        scene_timeline = []

        for idx, node_id in enumerate(sorted_nodes):
            node = dag.nodes[node_id]

            # Calculate anchors
            anchors = self.decomposer.calculate_working_memory_anchors(
                scene_timeline=scene_timeline,
                current_scene_idx=idx,
                dag=dag,
                current_concept_id=node_id
            )

            # Create a 15-35s scene with novel-style narrative
            duration = 20 # fixed for now

            if node.level == 0:
                pacing = "focused and slow"
                tone = "mysterious discovery"
                narrative = f"Let's define the fundamental axiom: {node.name}. {node.description}."
            else:
                pacing = "fast and dynamic"
                tone = "exciting synthesis"
                narrative = f"Now we combine what we know to understand {node.name}. {node.description}."

            av_stim = AVStimulusDirective(
                visual_pacing=pacing,
                color_contrast_cue="High contrast on new elements",
                motion_metaphor="Smooth transition indicating connection",
                audio_tone_shift=tone
            )

            scene = MicroSceneScript(
                scene_id=f"scene_{idx}",
                duration_seconds=duration,
                narrative_text=narrative,
                av_stimulus=av_stim,
                working_memory_anchors=anchors,
                primary_concept_id=node_id
            )

            scenes.append(scene)
            scene_timeline.append(node_id)

        return scenes
