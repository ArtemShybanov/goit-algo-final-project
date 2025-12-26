import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())  # Unique id for NetworkX nodes


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    # Recursively add nodes/edges into graph and compute positions for plotting
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / (2 ** layer)
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / (2 ** layer)
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root: Node) -> None:
    # Draw a binary tree
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [n[1]["color"] for n in tree.nodes(data=True)]
    labels = {n[0]: n[1]["label"] for n in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def heapify_list(values: list[int]) -> list[int]:
    # Convert an arbitrary list into a min-heap (in-place) and return the heap array
    heap = values[:]
    heapq.heapify(heap)
    return heap

# Convert heap array representation into a linked binary tree of Node objects
def heap_array_to_tree(heap: list[int], index: int = 0) -> Node | None:
    """
    For a heap array:
      left child index  = 2*i + 1
      right child index = 2*i + 2
    """
    if index >= len(heap):
        return None

    root = Node(heap[index])

    left_i = 2 * index + 1
    right_i = 2 * index + 2

    root.left = heap_array_to_tree(heap, left_i)
    root.right = heap_array_to_tree(heap, right_i)

    return root


def visualize_heap(values: list[int]) -> None:
    # Build heap array, convert to tree, then draw
    heap = heapify_list(values)
    root = heap_array_to_tree(heap)
    draw_tree(root)


if __name__ == "__main__":
    # Test case
    data = [10, 4, 5, 1, 3, 8, 2, 9, 7, 6]
    visualize_heap(data)