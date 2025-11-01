import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# ---------------------------------------------
# N-Queens Solver
# ---------------------------------------------
def solve_n_queens(board_size, num_queens):
    solutions = []
    board = [-1] * board_size

    def is_safe(row, col):
        for r in range(row):
            c = board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def backtrack(row=0, placed=0):
        if placed == num_queens:
            sol = [board[i] for i in range(board_size) if board[i] != -1]
            row_positions = [i for i in range(board_size) if board[i] != -1]
            solutions.append(list(zip(row_positions, sol)))
            return
        if row == board_size:
            return
        for col in range(board_size):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1, placed + 1)
                board[row] = -1
        backtrack(row + 1, placed)

    backtrack()
    return solutions


# ---------------------------------------------
# Visualization Function
# ---------------------------------------------


def visualize_board(solution, board_size, num_queens, queen_icon_path=None):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, board_size - 0.5)
    ax.set_ylim(-0.5, board_size - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Board colors (like chess.com)
    light_color = "#EEEED2"
    dark_color = "#769656"

    for i in range(board_size):
        for j in range(board_size):
            color = light_color if (i + j) % 2 == 0 else dark_color
            square = patches.Rectangle(
                (j - 0.5, i - 0.5),
                1, 1,
                facecolor=color,
                edgecolor='black',
                linewidth=0.5
            )
            ax.add_patch(square)

    # Place queens
    for row, col in solution:
        if queen_icon_path:
            try:
                img = mpimg.imread(queen_icon_path)
                imagebox = OffsetImage(img, zoom=0.08 * (8 / board_size))
                ab = AnnotationBbox(imagebox, (col, row), frameon=False)
                ax.add_artist(ab)
            except Exception as e:
                st.warning(f"⚠️ Could not load queen icon: {e}")
                ax.text(col, row, '♛', ha='center', va='center',
                        fontsize=400/board_size,
                        color='black' if (row+col)%2==0 else 'white')
        else:
            ax.text(col, row, '♛', ha='center', va='center',
                    fontsize=400/board_size,
                    color='black' if (row+col)%2==0 else 'white')

    plt.title(f"{num_queens}-Queens on {board_size}×{board_size} Board",
              fontsize=16, fontweight='bold', pad=15)

    st.pyplot(fig, clear_figure=True)



# ---------------------------------------------
# Streamlit App UI
# ---------------------------------------------
def main():
    st.set_page_config(page_title="N-Queens Visualizer", layout="centered", page_icon="♛")

    st.markdown(
        "<h1 style='text-align: center; color: #e63946;'>♛ N-Queens Visualizer ♛</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-size: 18px;'>Explore all valid non-attacking queen placements on a customizable chessboard.</p>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("⚙️ Configuration")
        board_size = st.slider("Board Size (N × N)", 3, 8, 4)
        num_queens = st.slider("Number of Queens", 1, board_size, min(8, board_size))
        randomize = st.checkbox("Show random valid solution", value=True)

    # Compute solutions
    with st.spinner("Calculating possible configurations..."):
        solutions = solve_n_queens(board_size, num_queens)

    # Display results
    st.success(f"✅ Total possible outcomes: **{len(solutions)}**")

    if len(solutions) > 0:
        st.write("### Visualizing one valid configuration:")
        if randomize:
            solution = random.choice(solutions)
        else:
            solution = solutions[0]
        visualize_board(solution, board_size, num_queens,queen_icon_path='/assets/queen.png')
    else:
        st.error("No valid configuration found for the selected inputs.")


if __name__ == "__main__":
    main()
