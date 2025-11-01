import heapq
import matplotlib.pyplot as plt
import streamlit as st

# =====================================================
# 🗺️ GRAPH DATA (Rounded Path Costs + Explicit Heuristics)
# =====================================================

GRAPH = {
    "A": {"B": 2, "C": 2},
    "B": {"A": 2, "D": 2, "J": 2, "E": 3},
    "C": {"A": 2, "D": 2, "K": 2},
    "D": {"B": 2, "C": 2, "F": 3, "K": 3},
    "E": {"B": 3, "J": 2, "I": 2, "G": 3},
    "F": {"D": 3, "G": 2, "L": 2},
    "G": {"E": 3, "F": 2, "I": 2, "H": 2, "M": 3},
    "H": {"G": 2, "N": 2},
    "I": {"E": 2, "G": 2, "J": 2},
    "J": {"B": 2, "E": 2, "I": 2},
    "K": {"C": 2, "D": 3, "L": 3},
    "L": {"K": 3, "F": 2, "M": 3},
    "M": {"L": 3, "G": 3, "N": 3},
    "N": {"H": 2, "M": 3}
}

HEURISTIC = {
    "A": 10, "B": 8, "C": 9, "D": 7, "E": 5, "F": 6,
    "G": 3, "H": 0, "I": 4, "J": 6, "K": 7, "L": 5,
    "M": 2, "N": 1
}

COORDS = {
    "A": (0, 0),
    "B": (2, 1),
    "C": (2, -1),
    "D": (4, 0),
    "E": (6, 1),
    "F": (6, -1),
    "G": (8, 0),
    "H": (10, 0),
    "I": (8, 2),
    "J": (4, 2),
    "K": (4, -2),
    "L": (6, -3),
    "M": (8, -2),
    "N": (10, -2)
}

# =====================================================
# 🧮 HELPER FUNCTIONS
# =====================================================

def heuristic(a, goal="H"):
    return HEURISTIC[a]

def reconstruct_path(came_from, current):
    path = [current]
    while came_from[current] is not None:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# =====================================================
# ⭐ A* SEARCH
# =====================================================

def a_star(start, goal):
    open_heap = [(heuristic(start, goal), 0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    closed = set()

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        if current in closed:
            continue

        if current == goal:
            return reconstruct_path(came_from, current)

        closed.add(current)
        for neighbor, cost in GRAPH[current].items():
            tentative_g = g_score[current] + cost
            f_score = tentative_g + heuristic(neighbor, goal)
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(open_heap, (f_score, tentative_g, neighbor))
    return None

# =====================================================
# 💨 GREEDY BEST-FIRST SEARCH
# =====================================================

def greedy_best_first(start, goal):
    open_heap = [(heuristic(start, goal), 0, start)]
    came_from = {start: None}
    visited = set()

    while open_heap:
        h, g, current = heapq.heappop(open_heap)
        if current in visited:
            continue
        if current == goal:
            return reconstruct_path(came_from, current)
        visited.add(current)
        for neighbor, cost in GRAPH[current].items():
            if neighbor not in visited:
                came_from[neighbor] = current
                new_g = g + cost
                heapq.heappush(open_heap, (heuristic(neighbor, goal), new_g, neighbor))
    return None

# =====================================================
# 🎨 VISUALIZATION
# =====================================================

def plot_graph(path=None, title="Search Graph"):
    fig, ax = plt.subplots(figsize=(10, 6))
    # Draw edges
    for node, neighbors in GRAPH.items():
        x1, y1 = COORDS[node]
        for neighbor, cost in neighbors.items():
            x2, y2 = COORDS[neighbor]
            ax.plot([x1, x2], [y1, y2], 'gray', linestyle='--', alpha=0.5)
            midx, midy = (x1 + x2)/2, (y1 + y2)/2
            ax.text(midx, midy + 0.1, str(cost), fontsize=8, color='gray')

    # Draw nodes
    for node, (x, y) in COORDS.items():
        ax.scatter(x, y, c="skyblue", s=300, edgecolors="black", zorder=2)
        ax.text(x, y + 0.25, f"{node}\nh={HEURISTIC[node]}", ha='center', fontsize=9, fontweight='bold')

    # Highlight path
    if path:
        xs = [COORDS[n][0] for n in path]
        ys = [COORDS[n][1] for n in path]
        ax.plot(xs, ys, 'r-', linewidth=3, label="Path", zorder=1)
        for n in path:
            ax.scatter(*COORDS[n], c="red", s=350, edgecolors="black", zorder=3)
        ax.legend()

    ax.set_title(title)
    ax.axis('equal')
    ax.axis('off')
    st.pyplot(fig)

# =====================================================
# 🚀 STREAMLIT APP
# =====================================================

def main():
    st.set_page_config(page_title="ChatSearchBot 3.0", page_icon="🤖", layout="centered")
    st.title("🤖 ChatSearchBot — Intelligent Pathfinder 🌍")
    st.markdown("### Choose start, goal and algorithm — visualize the shortest path live!")

    with st.sidebar:
        st.header("⚙️ Controls")
        start = st.selectbox("Start Node", list(GRAPH.keys()))
        goal = st.selectbox("Goal Node", list(GRAPH.keys()), index=len(GRAPH)-1)
        algo = st.radio("Algorithm", ["A*", "Greedy Best-First"])
        run = st.button("🚀 Run Search")

    st.subheader("🗺️ Map Visualization")
    plot_graph(title="Initial Map Overview")

    if run:
        st.divider()
        st.subheader(f"🔍 Searching {start} → {goal} using {algo}")
        if algo == "A*":
            path = a_star(start, goal)
        else:
            path = greedy_best_first(start, goal)

        if not path:
            st.error("⚠️ No path found.")
        else:
            st.success(f"✅ Path found: {' → '.join(path)}")
            plot_graph(path, title=f"{algo} Path: {start} → {goal}")

if __name__ == "__main__":
    main()
