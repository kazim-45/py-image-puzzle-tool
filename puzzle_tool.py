"""
╔══════════════════════════════════════════╗
║          PUZZLIFY  —  Image Puzzle Tool  ║
║          Requires: Pillow (pip install   ║
║          Pillow) + Python 3.8+           ║
╚══════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw
import random
import time
import math
import os


# ─── THEME ────────────────────────────────────────────────────────────────────

COLORS = {
    "bg":           "#0d0f14",
    "surface":      "#161923",
    "surface2":     "#1e2433",
    "border":       "#2a3045",
    "accent":       "#f0a500",
    "accent_dim":   "#b07800",
    "accent_glow":  "#f0c060",
    "text":         "#e8eaf0",
    "text_dim":     "#7a8099",
    "text_faint":   "#3d4460",
    "success":      "#4ade80",
    "danger":       "#f87171",
    "white":        "#ffffff",
}

FONTS = {
    "title":    ("Courier", 22, "bold"),
    "subtitle": ("Courier", 10, "normal"),
    "label":    ("Courier", 11, "bold"),
    "body":     ("Courier", 10, "normal"),
    "mono":     ("Courier", 13, "bold"),
    "small":    ("Courier", 9, "normal"),
    "btn":      ("Courier", 10, "bold"),
}

PIECE_COUNTS = [4, 6, 8, 9, 12, 16, 20, 25, 32]


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def get_grid(n):
    """Return (cols, rows) for n pieces — closest to square, wider than tall."""
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


def fmt_time(seconds):
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m:02d}:{s:02d}"


def make_round_rect(canvas, x1, y1, x2, y2, r=8, **kwargs):
    points = [
        x1+r, y1,  x2-r, y1,
        x2, y1,  x2, y1+r,
        x2, y2-r,  x2, y2,
        x2-r, y2,  x1+r, y2,
        x1, y2,  x1, y2-r,
        x1, y1+r,  x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ─── MAIN APPLICATION ─────────────────────────────────────────────────────────

class PuzzlifyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUZZLIFY")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])

        # State
        self.original_image   = None
        self.source_path      = None
        self.pieces           = []          # list of PIL images (original order)
        self.piece_imgs       = []          # list of PhotoImage (display order)
        self.order            = []          # current positions
        self.selected_idx     = None        # which tile is selected
        self.moves            = 0
        self.start_time       = None
        self.timer_running    = False
        self.solved           = False
        self.n_pieces         = tk.IntVar(value=9)

        # Canvas geometry
        self.BOARD_W = 520
        self.BOARD_H = 520
        self.THUMB_SIZE = (140, 105)

        self._build_ui()
        self._tick()

    # ── UI CONSTRUCTION ───────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Left panel
        left = tk.Frame(self, bg=COLORS["bg"], width=220)
        left.pack(side="left", fill="y", padx=(20, 0), pady=20)
        left.pack_propagate(False)

        self._build_left_panel(left)

        # ── Separator
        sep = tk.Frame(self, bg=COLORS["border"], width=1)
        sep.pack(side="left", fill="y", padx=18, pady=20)

        # ── Right panel (board)
        right = tk.Frame(self, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)

        self._build_right_panel(right)

    def _build_left_panel(self, parent):
        # Title
        tk.Label(parent, text="PUZZLIFY", font=("Courier", 26, "bold"),
                 fg=COLORS["accent"], bg=COLORS["bg"]).pack(anchor="w")
        tk.Label(parent, text="image puzzle engine", font=FONTS["small"],
                 fg=COLORS["text_dim"], bg=COLORS["bg"]).pack(anchor="w")

        self._spacer(parent, 18)

        # ── Thumbnail preview
        self.thumb_frame = tk.Frame(parent, bg=COLORS["surface"],
                                    highlightthickness=1,
                                    highlightbackground=COLORS["border"],
                                    width=self.THUMB_SIZE[0]+2,
                                    height=self.THUMB_SIZE[1]+2)
        self.thumb_frame.pack(anchor="w")
        self.thumb_frame.pack_propagate(False)

        self.thumb_label = tk.Label(self.thumb_frame,
                                    text="no image\nloaded",
                                    font=FONTS["small"],
                                    fg=COLORS["text_faint"],
                                    bg=COLORS["surface"],
                                    justify="center")
        self.thumb_label.pack(expand=True)

        self._spacer(parent, 14)

        # ── Load image button
        self._btn(parent, "[ LOAD IMAGE ]", self._load_image,
                  accent=True).pack(anchor="w", fill="x")

        self._spacer(parent, 20)

        # ── Piece count
        tk.Label(parent, text="PUZZLE PIECES", font=FONTS["label"],
                 fg=COLORS["text_dim"], bg=COLORS["bg"]).pack(anchor="w")

        self._spacer(parent, 6)

        grid_f = tk.Frame(parent, bg=COLORS["bg"])
        grid_f.pack(anchor="w")

        for i, n in enumerate(PIECE_COUNTS):
            row = i // 3
            col = i % 3
            rb = tk.Radiobutton(
                grid_f, text=str(n),
                variable=self.n_pieces, value=n,
                font=FONTS["btn"],
                fg=COLORS["text_dim"],
                selectcolor=COLORS["surface2"],
                activeforeground=COLORS["accent"],
                activebackground=COLORS["bg"],
                bg=COLORS["bg"],
                indicatoron=False,
                relief="flat",
                bd=0,
                width=4, height=1,
                cursor="hand2",
                command=self._on_piece_count_change,
            )
            rb.grid(row=row, column=col, padx=2, pady=2)

        self._spacer(parent, 20)

        # ── Start button
        self._btn(parent, "[ SHUFFLE & START ]", self._start_puzzle
                  ).pack(anchor="w", fill="x")

        self._spacer(parent, 8)

        # ── Reset / Solve
        ctrl_row = tk.Frame(parent, bg=COLORS["bg"])
        ctrl_row.pack(anchor="w", fill="x")
        self._btn(ctrl_row, "RESET", self._reset_puzzle, small=True
                  ).pack(side="left", expand=True, fill="x", padx=(0, 4))
        self._btn(ctrl_row, "SOLVE", self._solve_puzzle, small=True
                  ).pack(side="left", expand=True, fill="x")

        self._spacer(parent, 24)

        # ── Stats
        tk.Label(parent, text="STATS", font=FONTS["label"],
                 fg=COLORS["text_dim"], bg=COLORS["bg"]).pack(anchor="w")

        self._spacer(parent, 8)

        stat_frame = tk.Frame(parent, bg=COLORS["surface"],
                              highlightthickness=1,
                              highlightbackground=COLORS["border"])
        stat_frame.pack(fill="x")

        rows_data = [
            ("TIME",   "—",  "timer_val"),
            ("MOVES",  "0",  "moves_val"),
            ("PIECES", "—",  "pieces_val"),
            ("STATUS", "—",  "status_val"),
        ]

        for label, default, attr in rows_data:
            row = tk.Frame(stat_frame, bg=COLORS["surface"])
            row.pack(fill="x", padx=10, pady=4)
            tk.Label(row, text=label, font=FONTS["small"],
                     fg=COLORS["text_faint"], bg=COLORS["surface"],
                     width=7, anchor="w").pack(side="left")
            val = tk.Label(row, text=default, font=FONTS["mono"],
                           fg=COLORS["accent"], bg=COLORS["surface"], anchor="e")
            val.pack(side="right")
            setattr(self, attr, val)

        self._spacer(parent, 20)

        # ── Legend
        tk.Label(parent, text="HOW TO PLAY", font=FONTS["label"],
                 fg=COLORS["text_dim"], bg=COLORS["bg"]).pack(anchor="w")
        self._spacer(parent, 6)
        for line in [
            "① Load an image",
            "② Pick piece count",
            "③ Click SHUFFLE & START",
            "④ Click a piece to select",
            "⑤ Click another to swap",
            "⑥ Solve the puzzle!",
        ]:
            tk.Label(parent, text=line, font=FONTS["small"],
                     fg=COLORS["text_dim"], bg=COLORS["bg"],
                     anchor="w").pack(anchor="w")

    def _build_right_panel(self, parent):
        # Top info bar
        top = tk.Frame(parent, bg=COLORS["bg"])
        top.pack(fill="x", pady=(0, 10))

        self.board_title = tk.Label(top, text="load an image to begin",
                                    font=FONTS["label"], fg=COLORS["text_dim"],
                                    bg=COLORS["bg"])
        self.board_title.pack(side="left")

        self.solved_badge = tk.Label(top, text="✓ SOLVED",
                                     font=FONTS["label"], fg=COLORS["success"],
                                     bg=COLORS["bg"])

        # Board canvas
        self.canvas = tk.Canvas(
            parent,
            width=self.BOARD_W, height=self.BOARD_H,
            bg=COLORS["surface"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            cursor="hand2",
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        self._draw_empty_board()

        # Piece count indicator below board
        self.grid_label = tk.Label(parent, text="",
                                   font=FONTS["small"], fg=COLORS["text_faint"],
                                   bg=COLORS["bg"])
        self.grid_label.pack(pady=(8, 0))

    # ── WIDGET HELPERS ────────────────────────────────────────────────────────

    def _spacer(self, parent, h):
        tk.Frame(parent, bg=COLORS["bg"], height=h).pack()

    def _btn(self, parent, text, cmd, accent=False, small=False):
        fg = COLORS["bg"] if accent else COLORS["accent"]
        bg = COLORS["accent"] if accent else COLORS["surface2"]
        act_bg = COLORS["accent_glow"] if accent else COLORS["border"]
        font = FONTS["small"] if small else FONTS["btn"]

        btn = tk.Button(
            parent, text=text, command=cmd,
            font=font, fg=fg, bg=bg,
            activeforeground=fg, activebackground=act_bg,
            relief="flat", bd=0,
            padx=8, pady=5 if small else 8,
            cursor="hand2",
        )
        return btn

    # ── BOARD DRAWING ─────────────────────────────────────────────────────────

    def _draw_empty_board(self):
        self.canvas.delete("all")
        cx, cy = self.BOARD_W // 2, self.BOARD_H // 2
        self.canvas.create_text(cx, cy - 12, text="[ ]",
                                font=("Courier", 32, "bold"),
                                fill=COLORS["text_faint"])
        self.canvas.create_text(cx, cy + 24,
                                text="load an image and press  SHUFFLE & START",
                                font=FONTS["small"], fill=COLORS["text_faint"])

    def _draw_board(self):
        self.canvas.delete("all")
        if not self.pieces:
            return

        cols, rows = get_grid(len(self.pieces))
        pw = self.BOARD_W // cols
        ph = self.BOARD_H // rows

        self.tile_rects = []

        for idx, piece_idx in enumerate(self.order):
            col = idx % cols
            row = idx // cols
            x1 = col * pw
            y1 = row * ph
            x2 = x1 + pw
            y2 = y1 + ph
            cx = x1 + pw // 2
            cy = y1 + ph // 2

            is_correct = (idx == piece_idx)
            is_selected = (self.selected_idx == idx)

            # Piece image
            img = self.piece_imgs[piece_idx]
            self.canvas.create_image(cx, cy, image=img)

            # Overlay for selection / correct
            if is_selected:
                self.canvas.create_rectangle(
                    x1+2, y1+2, x2-2, y2-2,
                    outline=COLORS["accent"], width=3,
                )
                self.canvas.create_rectangle(
                    x1+5, y1+5, x2-5, y2-5,
                    outline=COLORS["accent_dim"], width=1,
                )
            elif is_correct and not self.solved:
                self.canvas.create_rectangle(
                    x1+2, y1+2, x2-2, y2-2,
                    outline=COLORS["success"], width=2,
                )

            # Grid lines
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=COLORS["bg"], width=2,
            )

            # Piece number (small)
            num_color = COLORS["accent"] if is_selected else COLORS["text_faint"]
            self.canvas.create_text(
                x1 + 10, y1 + 10,
                text=str(piece_idx + 1),
                font=FONTS["small"], fill=num_color, anchor="nw"
            )

            self.tile_rects.append((x1, y1, x2, y2))

        if self.solved:
            self._draw_solved_overlay()

    def _draw_solved_overlay(self):
        # Semi-transparent dark overlay
        self.canvas.create_rectangle(
            0, 0, self.BOARD_W, self.BOARD_H,
            fill=COLORS["bg"], stipple="gray50", outline=""
        )
        cx, cy = self.BOARD_W // 2, self.BOARD_H // 2
        self.canvas.create_text(
            cx, cy - 20,
            text="PUZZLE SOLVED",
            font=("Courier", 28, "bold"),
            fill=COLORS["accent"],
        )
        self.canvas.create_text(
            cx, cy + 20,
            text=f"{self.moves_val['text']} moves  ·  {self.timer_val['text']}",
            font=FONTS["body"],
            fill=COLORS["text_dim"],
        )

    # ── CORE LOGIC ────────────────────────────────────────────────────────────

    def _load_image(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff"),
                ("All files", "*.*"),
            ]
        )
        if not path:
            return

        try:
            img = Image.open(path).convert("RGB")
            self.original_image = img
            self.source_path = path

            # Thumbnail
            thumb = img.copy()
            thumb.thumbnail(self.THUMB_SIZE, Image.LANCZOS)
            self._thumb_tk = ImageTk.PhotoImage(thumb)
            self.thumb_label.config(image=self._thumb_tk, text="")

            fname = os.path.basename(path)
            if len(fname) > 22:
                fname = fname[:19] + "..."
            self.board_title.config(text=fname, fg=COLORS["text"])
            self.status_val.config(text="READY", fg=COLORS["accent"])
            self.solved_badge.pack_forget()
            self.solved = False

            # Auto-slice with current setting
            self._slice_image()
            self._draw_board()

        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")

    def _slice_image(self):
        if not self.original_image:
            return

        n = self.n_pieces.get()
        cols, rows = get_grid(n)

        # Fit image to board, crop to exact aspect
        target_w = self.BOARD_W
        target_h = self.BOARD_H
        img = self.original_image.copy()

        # Crop to board aspect ratio
        img_ratio = img.width / img.height
        board_ratio = target_w / target_h
        if img_ratio > board_ratio:
            new_w = int(img.height * board_ratio)
            offset = (img.width - new_w) // 2
            img = img.crop((offset, 0, offset + new_w, img.height))
        else:
            new_h = int(img.width / board_ratio)
            offset = (img.height - new_h) // 2
            img = img.crop((0, offset, img.width, offset + new_h))

        img = img.resize((target_w, target_h), Image.LANCZOS)

        pw = target_w // cols
        ph = target_h // rows

        self.pieces = []
        self.piece_imgs = []

        for row in range(rows):
            for col in range(cols):
                box = (col * pw, row * ph, (col+1) * pw, (row+1) * ph)
                piece = img.crop(box)
                self.pieces.append(piece)
                self.piece_imgs.append(ImageTk.PhotoImage(piece))

        self.order = list(range(n))
        self.pieces_val.config(text=f"{n}  ({cols}×{rows})")
        self.grid_label.config(text=f"{cols} columns × {rows} rows  ·  {pw}×{ph}px per piece")

    def _start_puzzle(self):
        if not self.original_image:
            messagebox.showinfo("No Image", "Please load an image first.")
            return

        self._slice_image()

        # Shuffle — guarantee not already solved
        n = len(self.order)
        for _ in range(1000):
            random.shuffle(self.order)
            if self.order != list(range(n)):
                break

        self.moves = 0
        self.moves_val.config(text="0", fg=COLORS["accent"])
        self.start_time = time.time()
        self.timer_running = True
        self.solved = False
        self.selected_idx = None
        self.solved_badge.pack_forget()
        self.status_val.config(text="PLAYING", fg=COLORS["success"])

        self._draw_board()

    def _on_canvas_click(self, event):
        if not self.pieces or self.solved:
            return

        cols, rows = get_grid(len(self.pieces))
        pw = self.BOARD_W // cols
        ph = self.BOARD_H // rows

        col = event.x // pw
        row = event.y // ph

        if col >= cols or row >= rows:
            return

        idx = row * cols + col
        if idx >= len(self.order):
            return

        if self.selected_idx is None:
            self.selected_idx = idx
        elif self.selected_idx == idx:
            self.selected_idx = None
        else:
            # Swap
            a, b = self.selected_idx, idx
            self.order[a], self.order[b] = self.order[b], self.order[a]
            self.moves += 1
            self.moves_val.config(text=str(self.moves))
            self.selected_idx = None
            self._check_solved()

        self._draw_board()

    def _check_solved(self):
        if self.order == list(range(len(self.pieces))):
            self.solved = True
            self.timer_running = False
            self.status_val.config(text="SOLVED!", fg=COLORS["success"])
            self.solved_badge.pack(side="right")
            self._draw_board()

    def _reset_puzzle(self):
        if not self.pieces:
            return
        n = len(self.pieces)
        self.order = list(range(n))
        self.moves = 0
        self.moves_val.config(text="0")
        self.start_time = None
        self.timer_running = False
        self.timer_val.config(text="—")
        self.selected_idx = None
        self.solved = False
        self.solved_badge.pack_forget()
        self.status_val.config(text="READY", fg=COLORS["accent"])
        self._draw_board()

    def _solve_puzzle(self):
        if not self.pieces:
            return
        self.order = list(range(len(self.pieces)))
        self.timer_running = False
        self.solved = True
        self.selected_idx = None
        self.status_val.config(text="SOLVED!", fg=COLORS["success"])
        self.solved_badge.pack(side="right")
        self._draw_board()

    def _on_piece_count_change(self):
        if self.original_image and not self.timer_running:
            self._slice_image()
            self._draw_board()

    # ── TIMER ─────────────────────────────────────────────────────────────────

    def _tick(self):
        if self.timer_running and self.start_time:
            elapsed = time.time() - self.start_time
            self.timer_val.config(text=fmt_time(elapsed))
        self.after(500, self._tick)


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = PuzzlifyApp()

    # Center window
    app.update_idletasks()
    w, h = app.winfo_width(), app.winfo_height()
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

    app.mainloop()
