# 🧠 AI Laboratory — Informed Search, N-Queens & 8-Tile Puzzle

![Python](https://img.shields.io/badge/Built%20with-Python-3776AB?logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)
![Pygame](https://img.shields.io/badge/Game%20Engine-Pygame-0A6D92?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> 🎯 *An interactive AI playground featuring Informed Search algorithms, the N-Queens problem, and a beautifully modern 8-Tile Puzzle — crafted with pure Python.*

---

## 🔍 Informed Search Algorithms

🚀 **[Live Demo →](https://ai-laboratory-informed-search.streamlit.app/)**  

Explore classic informed search strategies like **A\***, **Greedy Best-First**, and **Uniform Cost Search** — visualized step by step.

**✨ Features**
- Heuristic vs cost comparisons  
- Dynamic node expansion  
- Visual path reconstruction  

---

## 👑 N-Queens Problem

♟️ **[Live Demo →](https://ai-laboratory-n-queens-problem.streamlit.app/)**  

Watch the **N-Queens** problem come alive with real-time visualization and backtracking search.

**✨ Features**
- Configurable board size  
- Visual queen placement  
- Highlighted conflicts and valid states  

---

## 🧩 8-Tile Puzzle (Desktop Edition)

🎮 **[⬇️ Download for Windows (.exe)](https://github.com/yourusername/AI-Laboratory/releases/download/v1.0/tile_game.exe)**  

A sleek and modern twist on the classic **8-Puzzle Game**, powered by **Pygame** and **A\*** search.

**✨ Highlights**
- Click-to-move gameplay  
- Instant **A\*** auto-solver  
- Elegant dark UI with soft blue tiles  
- Real-time timer and move counter  
- Undo / Redo functionality  
- “🎉 Solved!” dialog popup when you win  

**🕹️ Controls**

| Key / Action | Description |
|---------------|-------------|
| 🖱️ Click Tile | Move block into the empty space |
| `N` | Start new random game |
| `A` | Auto-solve with A* |
| `U` | Undo last move |
| `R` | Redo previous move |

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend / Visualization** | Streamlit, Pygame |
| **AI Algorithms** | A\*, Greedy BFS, UCS, Backtracking |
| **Language** | Python 3.10+ |
| **Packaging** | PyInstaller |
| **Hosting** | Streamlit Cloud, GitHub Pages |

---

## 🧠 Local Setup

Clone and set up the project locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-Laboratory.git
cd AI-Laboratory

# Create a virtual environment
python -m venv venv
# (Windows)
venv\Scripts\activate
# (macOS / Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally (Pygame)
python tile_game.py
