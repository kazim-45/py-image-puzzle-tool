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
   Install dependencies

2. **Install dependenies**

   ```bash
   pip install Pillow
   
Note: Tkinter is included with standard Python installations on most systems.
If you're on Linux, you may need to install python3-tk separately.

3. **Run the application**

   ```bash
   python puzzle_tool.py
   
**🖱️ How to Play**
Click [ LOAD IMAGE ] and select any image file.

Choose the desired number of pieces from the radio buttons.

Press [ SHUFFLE & START ] to scramble the puzzle.

Click a tile – it will be highlighted in orange.

Click another tile – the two tiles swap positions.

Continue swapping until the image is fully restored.

When solved, the timer stops and a "PUZZLE SOLVED" overlay appears.

💡 Tip: Use RESET to start over with the same image, or SOLVE to finish instantly.

🧠 How It Works
Image slicing – The loaded image is cropped to the board’s aspect ratio, resized to fit exactly, and divided into cols × rows equal pieces (the grid is determined to be as square as possible for the given piece count).

Shuffling – The order of pieces is randomly permuted; a simple shuffle ensures it’s not accidentally solved.

Swapping – Clicking two different tiles swaps their positions in the order list. Each swap increments the move counter.

Solving detection – The puzzle is solved when the order list equals [0, 1, 2, … , n-1]. The timer stops and a success overlay appears.

UI – Built entirely with Tkinter’s native widgets and canvas. Custom colors and fonts create a modern, dark‑themed interface.

   ```markdown
![puzzlify interface]<img width="1222" height="958" alt="demo1" src="https://github.com/user-attachments/assets/7353fd12-576a-4270-afea-8824e402f629" /><img width="1227" height="952" alt="demo2" src="https://github.com/user-attachments/assets/653434f3-fbd6-4411-936e-20125ac23b49" /><img width="1220" height="977" alt="demo3" src="https://github.com/user-attachments/assets/c3458d83-bd6f-42aa-a48d-91ca54a6d57c" />


```

📁 Project Structure
text
puzzlify/
├── puzzle_tool.py          # Main application code
├── README.md               # This file
├── demo.gif                # Optional demonstration animation
└── LICENSE                 # MIT license
🔧 Future Improvements
Save/Load puzzle state

Different difficulty modes (e.g., limited moves)

Animated swaps

Sound effects on tile swap and solve

Leaderboard / best times

🤝 Contributing
Contributions, bug reports, and feature requests are welcome!
Feel free to open an issue or submit a pull request.

📄 License
Distributed under the MIT License. See LICENSE for more information.

👨‍💻 Author
Kazim Khan – https://kazimportfolio.vercel.app – [@alphamanofgod](https://www.instagram.com/alphamanofgod/)

Project Link: https://github.com/kazim-45/puzzlify
