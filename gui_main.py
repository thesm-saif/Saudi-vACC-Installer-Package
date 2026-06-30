import tkinter as tk
from PIL import Image, ImageTk
import os

from constants import (
    ASSETS_FOLDER, GREEN_PRIMARY, GOLD, WHITE,
    BG_DARK, BG_HEADER, BG_CARD, GREY_TEXT, GREY_DIM
)
from config import load_config, save_config
from gui_theme import open_theme_window
from gui_profile import open_profile_window

class MainApp:
    def __init__(self, root):
        self.root   = root
        self.config = load_config()
        self._refs  = []
        root.title("Saudi Arabian vACC - Configurator")
        root.resizable(False, False)
        root.configure(bg=BG_DARK)

        try:
            root.iconbitmap(os.path.join(ASSETS_FOLDER, "app.ico"))
        except Exception:
            pass

        try:
            ico = ImageTk.PhotoImage(
                Image.open(os.path.join(ASSETS_FOLDER, "app.png")).resize((32, 32))
            )
            root.iconphoto(True, ico)
            self._refs.append(ico)
        except Exception:
            pass

        self._build()

    def _build(self):
        WIN_W = 600
        tk.Frame(self.root, bg=GOLD, height=3).pack(fill="x")
        header = tk.Frame(self.root, bg=BG_HEADER)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=1)
        left = tk.Frame(header, bg=BG_HEADER)
        left.grid(row=0, column=0, sticky="w", padx=24, pady=16)

        try:
            raw = Image.open(os.path.join(ASSETS_FOLDER, "logo.png"))
            raw = raw.resize((60, 60), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(raw)
            tk.Label(left, image=logo_img, bg=BG_HEADER).pack(side="left")
            self._refs.append(logo_img)
        except Exception:
            pass

        tk.Label(
            header,
            text="Configurator",
            font=("Segoe UI", 16, "bold"),
            bg=BG_HEADER, fg=WHITE
        ).grid(row=0, column=1)

        tk.Label(
            header,
            text="© 2026 VATSIM Saudi Arabia",
            font=("Segoe UI", 8),
            bg=BG_HEADER, fg=GREY_TEXT
        ).grid(row=0, column=2, sticky="e", padx=24)

        tk.Frame(self.root, bg=GREY_DIM, height=1).pack(fill="x")
        btn_frame = tk.Frame(self.root, bg=BG_DARK)
        btn_frame.pack(fill="x", padx=60, pady=28)

        self._btn(btn_frame, "Change Colour Theme", self._open_theme)
        self._btn(btn_frame, "EuroScope Profile",   self._open_profile)

        tk.Frame(self.root, bg=GREY_DIM, height=1).pack(fill="x")
        tk.Label(
            self.root,
            text="© 2026 Saudi Arabian vACC",
            font=("Segoe UI", 8),
            bg=BG_DARK, fg=GREY_TEXT
        ).pack(pady=12)

        self.root.update_idletasks()
        h = self.root.winfo_reqheight()
        self.root.geometry(f"{WIN_W}x{h}")
        self.root.minsize(WIN_W, h)
        self.root.maxsize(WIN_W, h)

    def _btn(self, parent, text, command):
        frame = tk.Frame(parent, bg=GREY_DIM, pady=1, padx=1)
        frame.pack(fill="x", pady=6)
        btn = tk.Label(
            frame, text=text,
            font=("Segoe UI", 11), bg=BG_CARD, fg=WHITE,
            cursor="hand2", pady=12
        )
        btn.pack(fill="x")
        btn.bind("<Enter>",    lambda e: btn.configure(bg=GREEN_PRIMARY))
        btn.bind("<Leave>",    lambda e: btn.configure(bg=BG_CARD))
        btn.bind("<Button-1>", lambda e: command())

    def _open_theme(self):
        open_theme_window(self.root, self.config, save_config)

    def _open_profile(self):
        open_profile_window(self.root, self.config, save_config)