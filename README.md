# 🧩 Puzzlify – Image Puzzle Tool

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-10.0.0-green.svg)](https://python-pillow.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

Puzzlify is an interactive desktop puzzle game that transforms any image into a grid of movable tiles.  
Scramble the pieces, then restore the original image by swapping tiles.  
It's a fun brain teaser with clean visuals, stats tracking, and instant solve functionality.

![Puzzlify Demo](demo.gif) <!-- Add a screenshot or GIF here -->

---

## ✨ Features

- 📸 **Load any image** – Supports JPG, PNG, BMP, GIF, WebP, TIFF.
- 🧩 **Adjustable piece count** – Choose from 4 to 32 pieces (grids like 2×2 up to 8×4).
- 🎮 **Intuitive swapping** – Click a tile to select, then click another to swap.
- ⏱️ **Timer & move counter** – Track your solving progress.
- 🎨 **Visual feedback** – Selected tile highlight, correct tile outline, and a victory overlay.
- 🔄 **Reset & Solve** – Reset to original or instantly solve the puzzle.
- 📦 **Built‑in thumbnail preview** – See the loaded image in the left panel.
- 💻 **Lightweight GUI** – Uses Tkinter and Pillow – no external dependencies beyond standard libraries.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system.
- **Pillow** library – for image processing.

### Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/yourusername/puzzlify.git
   cd puzzlify