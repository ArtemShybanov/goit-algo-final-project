import uuid
import heapq
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="#87CEEB"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4()) # Unique id for NetworkX nodes


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


def build_nx_tree_and_pos(tree_root: Node):
    # Build NetworkX graph and positions once (so it doesn't recompute every frame)
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)
    return tree, pos


def draw_tree_frame(tree, pos, tree_root: Node, ax, title: str) -> None:
    # Draw a single frame into an existing matplotlib axes
    ax.clear()
    ax.set_title(title)

    colors = [tree.nodes[n]["color"] for n in tree.nodes()]
    labels = {n: tree.nodes[n]["label"] for n in tree.nodes()}

    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors, ax=ax)


def heapify_list(values: list[int]) -> list[int]:
    # Convert an arbitrary list into a min-heap (in-place) and return the heap array
    heap = values[:]
    heapq.heapify(heap)
    return heap

# Convert heap array representation into a linked binary tree of Node objects
def heap_array_to_tree(heap: list[int], index: int = 0) -> Node | None:
    if index >= len(heap):
        return None

    root = Node(heap[index])

    left_i = 2 * index + 1
    right_i = 2 * index + 2

    root.left = heap_array_to_tree(heap, left_i)
    root.right = heap_array_to_tree(heap, right_i)

    return root


def collect_nodes_bfs(root: Node) -> list[Node]:
    # Collect all nodes in BFS order (used only to know total node count for color gradient)
    q = deque([root])
    out: list[Node] = []

    while q:
        cur = q.popleft()
        out.append(cur)
        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)

    return out


def lerp(a: int, b: int, t: float) -> int:
    # Linear interpolation between integers a and b
    return int(a + (b - a) * t)


def hex_gradient(n: int, start_hex: str = "#0B2545", end_hex: str = "#BFEFFF") -> list[str]:
    """
    Create n HEX colors from dark -> light.
    Default: dark blue -> light blue.
    """
    start_hex = start_hex.lstrip("#")
    end_hex = end_hex.lstrip("#")

    sr, sg, sb = int(start_hex[0:2], 16), int(start_hex[2:4], 16), int(start_hex[4:6], 16)
    er, eg, eb = int(end_hex[0:2], 16), int(end_hex[2:4], 16), int(end_hex[4:6], 16)

    if n <= 1:
        return [f"#{start_hex}"]

    colors = []
    for i in range(n):
        t = i / (n - 1)
        r = lerp(sr, er, t)
        g = lerp(sg, eg, t)
        b = lerp(sb, eb, t)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")

    return colors


def reset_colors(root: Node, color: str = "#87CEEB") -> None:
    # Reset all node colors to a base color (iterative BFS, no recursion)
    q = deque([root])
    while q:
        cur = q.popleft()
        cur.color = color
        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)


def dfs_preorder_stack(root: Node) -> list[Node]:
    """
    DFS traversal using a stack (without recursion).
    Preorder: Node -> Left -> Right
    """
    stack = [root]
    order = []

    while stack:
        cur = stack.pop()
        order.append(cur)

        # Push right first so left is processed first (LIFO stack)
        if cur.right:
            stack.append(cur.right)
        if cur.left:
            stack.append(cur.left)

    return order


def bfs_queue(root: Node) -> list[Node]:
    """
    BFS traversal using a queue (without recursion).
    Level order: left to right at each level
    """
    q = deque([root])
    order = []

    while q:
        cur = q.popleft()
        order.append(cur)

        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)

    return order


def visualize_traversal_steps(root: Node, visit_order: list[Node], traversal_name: str, delay: float = 0.8) -> None:
    # Animate traversal in a single window using pause()
    total = len(visit_order)
    palette = hex_gradient(total, start_hex="#0B2545", end_hex="#BFEFFF")

    reset_colors(root, color="#87CEEB")

    tree, pos = build_nx_tree_and_pos(root)
    fig, ax = plt.subplots(figsize=(10, 6))

    plt.ion() # interactive mode on

    for step, node in enumerate(visit_order, start=1):
        node.color = palette[step - 1]

        # NetworkX stores color/label in graph attributes, update them from Node objects
        # Rebuild node attributes each frame by reading from the Node instances
        # This loop is iterative BFS, no recursion
        q = deque([root])
        while q:
            cur = q.popleft()
            tree.nodes[cur.id]["color"] = cur.color
            tree.nodes[cur.id]["label"] = cur.val
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)

        draw_tree_frame(tree, pos, root, ax, title=f"{traversal_name}: step {step}/{total} (visited {node.val})")
        plt.pause(delay)

    plt.ioff() # interactive mode off
    


if __name__ == "__main__":
    # Build a heap - convert to tree - visualize
    values = [10, 4, 5, 1, 3, 8, 2, 9, 7, 6]
    heap = heapify_list(values)
    root = heap_array_to_tree(heap)

    # DFS (stack)
    dfs_order = dfs_preorder_stack(root)
    visualize_traversal_steps(root, dfs_order, traversal_name="DFS (stack, preorder)")

    # BFS (queue)
    bfs_order = bfs_queue(root)
    visualize_traversal_steps(root, bfs_order, traversal_name="BFS (queue, level-order)")

    plt.show() # final blocking show so the last frame stays