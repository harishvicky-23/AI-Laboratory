import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

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
def visualize_board(solution, board_size, num_queens):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, board_size - 0.5)
    ax.set_ylim(-0.5, board_size - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()

    # Draw chessboard
    for i in range(board_size):
        for j in range(board_size):
            color = "#f0d9b5" if (i + j) % 2 == 0 else "#b58863"  # light/dark wood tones
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)

    # Place queens (♛ symbol centered perfectly)
    for row, col in solution:
        ax.text(col, row, '♛', ha='center', va='center', fontsize=500/board_size, color='crimson')

    plt.title(f"{num_queens}-Queens on {board_size}×{board_size} Board", fontsize=14, fontweight='bold')
    st.pyplot(fig)


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
        board_size = st.slider("Board Size (N × N)", 4, 12, 8)
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
        visualize_board(solution, board_size, num_queens)
    else:
        st.error("No valid configuration found for the selected inputs.")


if __name__ == "__main__":
    main()
