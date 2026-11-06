from backend.core_ingestion.interfaces import ConceptDependencyDAG, AtomicConceptNode, WorkingMemoryAnchor
from typing import List, Dict, Tuple
from collections import defaultdict, deque

class CycleDetectedException(Exception):
    pass

class CognitiveDecomposer:
    def __init__(self):
        pass

    def decompose(self, content: str) -> ConceptDependencyDAG:
        # Mocking the LLM decomposition for this implementation
        # A real implementation would prompt an LLM to extract these concepts and prerequisites
        nodes = {
            "node": AtomicConceptNode(id="node", name="Node", description="A basic data structure element", level=0, prerequisites=[]),
            "ptr": AtomicConceptNode(id="ptr", name="Pointer", description="A reference to another node", level=0, prerequisites=[]),
            "bst_inv": AtomicConceptNode(id="bst_inv", name="BST Invariant", description="Left < Parent < Right", level=0, prerequisites=[]),
            "bst": AtomicConceptNode(id="bst", name="Binary Search Tree", description="A tree structure", level=1, prerequisites=["node", "ptr", "bst_inv"]),
            "bst_rot": AtomicConceptNode(id="bst_rot", name="BST Rotation", description="Rotating nodes to balance the tree", level=2, prerequisites=["bst"])
        }

        dag = ConceptDependencyDAG(nodes=nodes, root_id="bst_rot")

        # Validate and Topologically sort
        self.topological_sort(dag)

        return dag

    def topological_sort(self, dag: ConceptDependencyDAG) -> List[str]:
        """
        Uses Kahn's algorithm for topological sorting and cycle detection.
        Assigns bottom-up levels.
        """
        in_degree = {node_id: 0 for node_id in dag.nodes}
        adj_list = defaultdict(list)

        for node_id, node in dag.nodes.items():
            for prereq in node.prerequisites:
                adj_list[prereq].append(node_id)
                in_degree[node_id] += 1

        queue = deque([node_id for node_id in in_degree if in_degree[node_id] == 0])
        sorted_order = []

        # For level assignment
        levels = {node_id: 0 for node_id in dag.nodes}

        visited_count = 0
        while queue:
            curr = queue.popleft()
            sorted_order.append(curr)
            visited_count += 1

            dag.nodes[curr].level = levels[curr]

            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                levels[neighbor] = max(levels[neighbor], levels[curr] + 1)
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if visited_count != len(dag.nodes):
            raise CycleDetectedException("Cycle detected in ConceptDependencyDAG")

        return sorted_order

    def calculate_working_memory_anchors(self, scene_timeline: List[str], current_scene_idx: int, dag: ConceptDependencyDAG, current_concept_id: str) -> List[WorkingMemoryAnchor]:
        """
        Calculates working memory anchors for a given scene.
        Rule: If a concept was introduced >2 scenes ago and is a prerequisite for the current concept, attach an anchor.
        """
        anchors = []
        concept = dag.nodes[current_concept_id]

        for prereq_id in concept.prerequisites:
            # Find when this prereq was introduced
            try:
                intro_idx = scene_timeline.index(prereq_id)
                if current_scene_idx - intro_idx > 2:
                    anchors.append(
                        WorkingMemoryAnchor(
                            concept_id=prereq_id,
                            visual_reminder=f"Icon for {dag.nodes[prereq_id].name}"
                        )
                    )
            except ValueError:
                # If prerequisite not in timeline yet, it's assumed prior knowledge, add anchor anyway
                anchors.append(
                    WorkingMemoryAnchor(
                        concept_id=prereq_id,
                        visual_reminder=f"Icon for {dag.nodes[prereq_id].name}"
                    )
                )

        return anchors
