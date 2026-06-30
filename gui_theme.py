import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os

from constants import (
    ASSETS_FOLDER, SETTINGS_FILE,
    GREEN_PRIMARY, GREEN_HOVER, GOLD, WHITE,
    BG_DARK, BG_CARD, BG_CARD_ACTIVE, BG_HEADER,
    GREY_TEXT, GREY_DIM, BORDER_DEFAULT, BORDER_ACTIVE,
    CARD_W, CARD_IMG_H, CARD_FOOT_H, CARD_GAP, SIDE_PAD,
    HEADER_H, FOLDER_H, LABEL_GAP_TOP, LABEL_H,
    LABEL_GAP_BOTTOM, CARDS_GAP_BOTTOM, BOTTOM_H,
    THEME_NAMES, THEME_DESCRIPTIONS,
)
from theme_switcher import read_themes, apply_theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def open_theme_window(parent, config, save_config_fn):
    win = ctk.CTkToplevel(parent)
    win.title("Saudi Arabian vACC - Theme Switcher")
    win.resizable(False, False)
    win.configure(fg_color=BG_DARK)
    win.grab_set()

    try:
        win.iconbitmap(os.path.join(ASSETS_FOLDER, "app.ico"))
    except Exception:
        pass

    num   = len(THEME_NAMES)
    win_w = SIDE_PAD * 2 + CARD_W * num + CARD_GAP * (num - 1)
    win_h = (
        HEADER_H
        + FOLDER_H
        + LABEL_GAP_TOP + LABEL_H + LABEL_GAP_BOTTOM
        + (CARD_IMG_H + CARD_FOOT_H)
        + CARDS_GAP_BOTTOM
        + BOTTOM_H
    )
    win.geometry(f"{win_w}x{win_h}")
    win.minsize(win_w, win_h)
    win.maxsize(win_w, win_h)

    selected   = ctk.StringVar(value=THEME_NAMES[0])
    cards      = {}
    refs       = []

    saved_folder = config.get("sector_folder", "")
    folder_var   = ctk.StringVar(
        value=saved_folder if saved_folder else "No installation package selected"
    )

    def highlight(name):
        for n, card in cards.items():
            card.configure(
                border_color=BORDER_ACTIVE if n == name else BORDER_DEFAULT,
                fg_color=BG_CARD_ACTIVE if n == name else BG_CARD
            )

    def on_select(name):
        selected.set(name)
        highlight(name)
        status_var.set(f"{name.title()} Theme selected.")

    ctk.CTkFrame(win, height=3, fg_color=GOLD, corner_radius=0).pack(fill="x")
    header = ctk.CTkFrame(win, fg_color=BG_HEADER, height=HEADER_H - 3, corner_radius=0)
    header.pack(fill="x")
    header.pack_propagate(False)
    left = ctk.CTkFrame(header, fg_color="transparent")
    left.place(relx=0.0, rely=0.5, anchor="w", x=SIDE_PAD)
    try:
        logo_img = ctk.CTkImage(
            Image.open(os.path.join(ASSETS_FOLDER, "logo.png")), size=(70, 70)
        )
        ctk.CTkLabel(left, image=logo_img, text="").pack(side="left")
        refs.append(logo_img)
    except Exception:
        pass

    ctk.CTkLabel(
        header, text="Themes",
        font=ctk.CTkFont("Segoe UI", 24, weight="bold"), text_color=WHITE
    ).place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        header, text="© 2026 VATSIM Saudi Arabia",
        font=ctk.CTkFont("Segoe UI", 9), text_color=GREY_TEXT
    ).place(relx=1.0, rely=0.5, anchor="e", x=-SIDE_PAD)

    ctk.CTkFrame(win, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")
    folder_bar = ctk.CTkFrame(win, fg_color="#141414", height=FOLDER_H, corner_radius=0)
    folder_bar.pack(fill="x")
    folder_bar.pack_propagate(False)

    fi = ctk.CTkFrame(folder_bar, fg_color="transparent")
    fi.pack(fill="both", expand=True, padx=SIDE_PAD, pady=12)

    ctk.CTkLabel(
        fi, text="INSTALLATION\nPACKAGE",
        font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT,
        width=110, anchor="w", justify="left"
    ).pack(side="left")

    folder_lbl = ctk.CTkLabel(
        fi, textvariable=folder_var,
        font=ctk.CTkFont("Segoe UI", 10),
        text_color=WHITE if saved_folder else GREY_TEXT,
        fg_color=BG_CARD, corner_radius=5, anchor="w", padx=12
    )
    folder_lbl.pack(side="left", fill="both", expand=True)

    def browse():
        folder = filedialog.askdirectory(
            title="Select your sector file installation package", parent=win
        )
        if folder:
            folder_var.set(folder)
            folder_lbl.configure(text_color=WHITE)
            config["sector_folder"] = folder
            save_config_fn(config)
            status_var.set("Installation package set — select a theme and click Apply Theme.")

    ctk.CTkButton(
        fi, text="Browse",
        font=ctk.CTkFont("Segoe UI", 10, weight="bold"),
        fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, text_color=WHITE,
        corner_radius=5, width=88, command=browse
    ).pack(side="left", padx=(10, 0), fill="y")

    ctk.CTkFrame(win, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")
    lw = ctk.CTkFrame(win, fg_color="transparent", height=LABEL_H)
    lw.pack(fill="x", padx=SIDE_PAD, pady=(LABEL_GAP_TOP, LABEL_GAP_BOTTOM))
    lw.pack_propagate(False)
    ctk.CTkLabel(
        lw, text="SELECT A COLOUR THEME",
        font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, anchor="w"
    ).pack(fill="both", expand=True)

    cards_row = ctk.CTkFrame(win, fg_color="transparent",
                              height=CARD_IMG_H + CARD_FOOT_H)
    cards_row.pack(fill="x", padx=SIDE_PAD, pady=(0, CARDS_GAP_BOTTOM))
    cards_row.pack_propagate(False)

    for i, name in enumerate(THEME_NAMES):
        is_last = (i == len(THEME_NAMES) - 1)
        card = ctk.CTkFrame(
            cards_row, fg_color=BG_CARD, corner_radius=10,
            border_width=1, border_color=BORDER_DEFAULT,
            width=CARD_W, height=CARD_IMG_H + CARD_FOOT_H
        )
        card.pack(side="left", padx=(0, 0 if is_last else CARD_GAP))
        card.pack_propagate(False)
        cards[name] = card

        img_box = ctk.CTkFrame(card, fg_color="transparent",
                                width=CARD_W - 24, height=CARD_IMG_H - 12)
        img_box.pack(padx=12, pady=(12, 0))
        img_box.pack_propagate(False)

        preview_path = os.path.join(ASSETS_FOLDER, f"{name}.png")
        if os.path.exists(preview_path):
            try:
                raw      = Image.open(preview_path)
                tw, th   = CARD_W - 24, CARD_IMG_H - 12
                sr       = raw.width / raw.height
                br       = tw / th
                if sr > br:
                    nh, nw = th, int(th * sr)
                else:
                    nw, nh = tw, int(tw / sr)
                resized  = raw.resize((nw, nh))
                l        = (nw - tw) // 2
                t        = (nh - th) // 2
                cropped  = resized.crop((l, t, l + tw, t + th))
                pimg     = ctk.CTkImage(cropped, size=(tw, th))
                lbl      = ctk.CTkLabel(img_box, image=pimg, text="")
                lbl.place(x=0, y=0)
                refs.append(pimg)
                lbl.bind("<Button-1>", lambda e, n=name: on_select(n))
            except Exception:
                _placeholder(img_box, name)
        else:
            _placeholder(img_box, name)

        ctk.CTkFrame(card, height=1, fg_color=GREY_DIM, corner_radius=0).pack(
            fill="x", padx=12, pady=(10, 0)
        )

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 12))

        ctk.CTkRadioButton(
            row, text="", variable=selected, value=name,
            fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, border_color="#555555",
            width=20, command=lambda n=name: on_select(n)
        ).pack(side="left")

        txt = ctk.CTkFrame(row, fg_color="transparent")
        txt.pack(side="left", padx=(10, 0))

        ctk.CTkLabel(
            txt, text=name.title() + " Theme",
            font=ctk.CTkFont("Segoe UI", 13, weight="bold"), text_color=WHITE, anchor="w"
        ).pack(anchor="w")

        desc = THEME_DESCRIPTIONS.get(name.upper(), "")
        if desc:
            ctk.CTkLabel(
                txt, text=desc,
                font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, anchor="w"
            ).pack(anchor="w")

        for w in (card, row, txt):
            w.bind("<Button-1>", lambda e, n=name: on_select(n))

    win._refs = refs
    highlight(THEME_NAMES[0])

    ctk.CTkFrame(win, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")
    bottom = ctk.CTkFrame(win, fg_color=BG_HEADER, height=BOTTOM_H, corner_radius=0)
    bottom.pack(fill="x", side="bottom")
    bottom.pack_propagate(False)

    bi = ctk.CTkFrame(bottom, fg_color="transparent")
    bi.pack(fill="both", expand=True, padx=SIDE_PAD, pady=14)

    status_var = ctk.StringVar(
        value="Browse to your sector file installation package, then select a theme."
    )
    ctk.CTkLabel(
        bi, textvariable=status_var,
        font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, anchor="w"
    ).pack(side="left", fill="both", expand=True)

    def on_apply():
        folder = config.get("sector_folder", "")
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning(
                "No Folder",
                "Please browse to your installation package first.", parent=win
            )
            return
        theme = selected.get()
        status_var.set(f"Applying {theme.title()} Theme...")
        apply_btn.configure(state="disabled", text="Applying...")
        win.update()
        try:
            themes = read_themes(SETTINGS_FILE)
            apply_theme(theme, themes, folder)
            status_var.set(f"{theme.title()} Theme applied. Reload EuroScope to see changes.")
            apply_btn.configure(state="normal", text="Apply Theme")
            messagebox.showinfo(
                "Theme Applied",
                f'"{theme.title()} Theme" applied.\n\nReload EuroScope to see the changes.',
                parent=win
            )
        except Exception as e:
            status_var.set("Error — see popup for details.")
            apply_btn.configure(state="normal", text="Apply Theme")
            messagebox.showerror("Error", str(e), parent=win)

    ctk.CTkButton(
        bi, text="Cancel",
        font=ctk.CTkFont("Segoe UI", 11),
        fg_color=GREY_DIM, hover_color="#3a3a3a", text_color=WHITE,
        corner_radius=6, width=88, command=win.destroy
    ).pack(side="right", padx=(10, 0), fill="y")

    apply_btn = ctk.CTkButton(
        bi, text="Apply Theme",
        font=ctk.CTkFont("Segoe UI", 11, weight="bold"),
        fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, text_color=WHITE,
        corner_radius=6, width=130, command=on_apply
    )
    apply_btn.pack(side="right", fill="y")


def _placeholder(parent, name):
    colors = {"DEFAULT": "#3a3a3a", "DARK": "#0d1117"}
    parent.configure(fg_color=colors.get(name, "#2a2a2a"))
    ctk.CTkLabel(
        parent, text="Preview coming soon",
        font=ctk.CTkFont("Segoe UI", 10), text_color="#555555"
    ).place(relx=0.5, rely=0.5, anchor="center")