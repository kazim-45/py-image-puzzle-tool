# 🧩 Puzzlify – Image Puzzle Tool

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-10.0.0-green.svg)](https://python-pillow.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

**Puzzlify** transforms any image into an interactive swap-tile puzzle. Load your favorite photo, scramble the pieces, and race against the clock to restore the original image. Perfect for brain training or just relaxing with a visual challenge.

---

## ✨ Features

| Category | Description |
|----------|-------------|
| 📸 **Image Loading** | Load any common image format (JPG, PNG, BMP, GIF, WebP, TIFF) |
| 🧩 **Flexible Grids** | Choose from 9 piece counts: 4, 6, 8, 9, 12, 16, 20, 25, or 32 pieces |
| 🎮 **Intuitive Controls** | Click a tile to select → click another to swap |
| ⏱️ **Stats Tracking** | Real-time timer and move counter during gameplay |
| 🎨 **Visual Feedback** | Orange highlight for selected tiles, green outline for correct placements |
| 🔄 **Game Controls** | Shuffle & Start, Reset, and Solve (instant completion) |
| 🖼️ **Thumbnail Preview** | See your loaded image in the left panel |
| 💻 **Lightweight** | Pure Python with Tkinter + Pillow – no heavy dependencies |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Pillow library for image processing

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/puzzlify.git
cd puzzlify

# Install dependencies
pip install Pillow

# Run the game
python puzzle_tool.py
```

> **Note:** Tkinter is included with Python on Windows and macOS.  
> On Linux, install it with: `sudo apt-get install python3-tk`

---

## 🎮 How to Play

1. **Load an Image**  
   Click `[ LOAD IMAGE ]` and select any photo from your computer.

2. **Choose Difficulty**  
   Select the number of puzzle pieces (more pieces = harder puzzle).

3. **Shuffle & Start**  
   Click `[ SHUFFLE & START ]` to scramble the tiles and begin the timer.

4. **Swap Tiles**  
   - **Click** a tile to select it (orange border appears)
   - **Click** another tile to swap positions
   - Continue until the image is fully restored

5. **Win!**  
   When all tiles are in place, a victory overlay appears with your final stats.

### Additional Controls

| Button | Function |
|--------|----------|
| **RESET** | Restores the puzzle to the solved state (keeps current image) |
| **SOLVE** | Instantly completes the puzzle (useful for seeing the final image) |

---

## 🧠 Technical Deep Dive

### Image Processing Pipeline

```
Original Image → Crop to Aspect Ratio → Resize to Board (520×520) 
→ Calculate Optimal Grid (cols × rows) → Slice into Pieces 
→ Store in Memory → Display on Canvas
```

### Grid Calculation Logic

The tool automatically determines the optimal grid layout to be as square as possible while exactly matching the chosen piece count:

```python
def get_grid(n):
    """Returns (cols, rows) for n pieces — closest to square, wider than tall."""
    best = (n, 1)
    best_diff = n - 1
    for c in range(2, n + 1):
        if n % c == 0:
            r = n // c
            diff = abs(c - r)
            if diff < best_diff or (diff == best_diff and c >= r):
                best_diff = diff
                best = (c, r)
    cols, rows = best
    if cols < rows:
        cols, rows = rows, cols
    return cols, rows
```

### Swap & Solve Mechanics

- **Swap Algorithm:** Two tiles exchange positions in the order list; each swap increments the move counter
- **Win Detection:** Puzzle is solved when `order == [0, 1, 2, ..., n-1]`
- **Timer:** Real-time tracking that stops automatically on solution

### UI Architecture

- **Left Panel:** Controls, image preview, stats, and instructions
- **Right Panel:** Interactive canvas displaying the puzzle grid
- **Theme:** Custom dark color scheme with accent colors for better visibility
- **Responsive:** Automatically adjusts piece dimensions based on grid size

---

## 📁 Project Structure

```
puzzlify/
├── puzzle_tool.py          # Main application (800+ lines of code)
├── demo1.png               # Start screen screenshot
├── demo2.png               # Loaded image screenshot  
├── demo3.png               # Active gameplay screenshot
├── README.md               # This file
└── LICENSE                 # MIT License
```

---

## 🛠️ Built With

- **[Python 3.8+](https://www.python.org/)** – Core programming language
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** – GUI framework (built-in)
- **[Pillow (PIL)](https://python-pillow.org/)** – Image processing library

---

## 🎯 Future Roadmap

- [ ] **Save/Load State** – Resume puzzles later
- [ ] **Difficulty Modes** – Limited moves, timed challenges
- [ ] **Animations** – Smooth tile swaps and transitions
- [ ] **Sound Effects** – Feedback sounds for swaps and solves
- [ ] **Leaderboard** – Track best times locally
- [ ] **Custom Themes** – Multiple color schemes
- [ ] **Keyboard Shortcuts** – Faster navigation

---

## 🤝 Contributing

Contributions are welcome! Whether it's:

- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🔧 Pull requests

Please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**KAZIM KHAN**  
- Portfolio: [kazimportfolio](https://kazimportfolio.vercel.app)  
- GitHub: [kazim-45](https://github.com/kazim-45)  
- Project Link: [github.com/kazim-45/puzzlify](https://github.com/kazim-45/puzzlify)

---

## 🙏 Acknowledgments

- Inspired by classic sliding puzzles and modern brain training apps
- Built with Python's excellent Tkinter and Pillow libraries
- Special thanks to the open-source community

---

## ⭐ Show Your Support

If you found this project useful, please give it a star ⭐ on GitHub!  
It helps others discover the project and motivates further development.

---

*Made with 🧩 and ☕*
