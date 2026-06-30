import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os

from constants import (
    ASSETS_FOLDER, GREEN_PRIMARY, GREEN_HOVER, GOLD, WHITE,
    BG_DARK, BG_CARD, BG_HEADER, GREY_TEXT, GREY_DIM,
    SIDE_PAD, HEADER_H, FOLDER_H, BOTTOM_H,
    RATINGS, RATING_MAP, RATING_VALUE_TO_LABEL,
)
from configurator import apply_configuration, read_profile_from_prf

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

WIN_W = 620

def open_profile_window(parent, config, save_config_fn):
    win = ctk.CTkToplevel(parent)
    win.title("Saudi Arabian vACC - EuroScope Profile")
    win.resizable(False, False)
    win.configure(fg_color=BG_DARK)
    win.grab_set()

    try:
        win.iconbitmap(os.path.join(ASSETS_FOLDER, "app.ico"))
    except Exception:
        pass

    refs = []
    existing = {}
    folder = config.get("sector_folder", "")

    if folder and os.path.isdir(folder):
        prf_files = [
            f for f in os.listdir(folder) if f.lower().endswith(".prf")
        ]
        if prf_files:
            existing = read_profile_from_prf(
                os.path.join(folder, prf_files[0])
            )

    ctk.CTkFrame(win, height=3, fg_color=GOLD, corner_radius=0).pack(fill="x")
    header = ctk.CTkFrame(win, fg_color=BG_HEADER, height=HEADER_H - 3, corner_radius=0)
    header.pack(fill="x")
    header.pack_propagate(False)
    left = ctk.CTkFrame(header, fg_color="transparent")
    left.place(relx=0.0, rely=0.5, anchor="w", x=SIDE_PAD)
    try:
        logo_img = ctk.CTkImage(
            Image.open(os.path.join(ASSETS_FOLDER, "logo.png")), size=(56, 56)
        )
        ctk.CTkLabel(left, image=logo_img, text="").pack(side="left")
        refs.append(logo_img)
    except Exception:
        pass

    ctk.CTkLabel(
        header, text="EuroScope Profile",
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
        fi, text="SECTOR FOLDER",
        font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT,
        width=110, anchor="w"
    ).pack(side="left")

    saved_folder = config.get("sector_folder", "")
    folder_var   = ctk.StringVar(
        value=saved_folder if saved_folder else "No folder selected"
    )

    folder_lbl = ctk.CTkLabel(
        fi, textvariable=folder_var,
        font=ctk.CTkFont("Segoe UI", 10),
        text_color=WHITE if saved_folder else GREY_TEXT,
        fg_color=BG_CARD, corner_radius=5, anchor="w", padx=12
    )
    folder_lbl.pack(side="left", fill="both", expand=True)

    def browse():
        f = filedialog.askdirectory(
            title="Select your sector file folder", parent=win
        )
        if f:
            folder_var.set(f)
            folder_lbl.configure(text_color=WHITE)
            config["sector_folder"] = f
            save_config_fn(config)
            _reload_existing(f)

    ctk.CTkButton(
        fi, text="Browse",
        font=ctk.CTkFont("Segoe UI", 10, weight="bold"),
        fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, text_color=WHITE,
        corner_radius=5, width=88, command=browse
    ).pack(side="left", padx=(10, 0), fill="y")

    ctk.CTkFrame(win, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")
    ctk.CTkLabel(
        win, text="CONTROLLER DETAILS",
        font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT
    ).pack(anchor="w", padx=SIDE_PAD, pady=(20, 10))

    form = ctk.CTkFrame(win, fg_color="transparent")
    form.pack(fill="x", padx=SIDE_PAD, pady=(0, 16))

    def make_entry(parent, label, masked=False, prefill=""):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT,
            width=100, anchor="w"
        ).pack(side="left")
        e = ctk.CTkEntry(
            row,
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color=BG_CARD, border_color=GREY_DIM,
            text_color=WHITE, show="*" if masked else "",
            corner_radius=5, height=36
        )
        e.pack(side="left", fill="x", expand=True)
        if prefill:
            e.insert(0, prefill)
        return e

    e_name     = make_entry(form, "Real Name", prefill=existing.get("realname", ""))
    e_cid      = make_entry(form, "CID",       masked=False,
                             prefill=existing.get("certificate", ""))
    e_password = make_entry(form, "Password",  masked=True,
                             prefill=existing.get("password", ""))

    rating_row = ctk.CTkFrame(form, fg_color="transparent")
    rating_row.pack(fill="x", pady=(0, 8))

    ctk.CTkLabel(
        rating_row, text="Rating",
        font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT,
        width=100, anchor="w"
    ).pack(side="left")

    existing_rating_num = int(existing.get("rating", "1"))
    default_rating = RATING_VALUE_TO_LABEL.get(existing_rating_num, RATINGS[0])

    rating_var = ctk.StringVar(value=default_rating)
    code_var   = ctk.StringVar(value=RATING_MAP[default_rating][1])

    ctk.CTkOptionMenu(
        rating_row,
        values=RATINGS,
        variable=rating_var,
        font=ctk.CTkFont("Segoe UI", 10),
        fg_color=BG_CARD,
        button_color=GREEN_PRIMARY,
        button_hover_color=GREEN_HOVER,
        text_color=WHITE,
        dropdown_fg_color="#1e1e1e",
        dropdown_text_color=WHITE,
        dropdown_hover_color=GREY_DIM,
        corner_radius=5, height=36,
        dynamic_resizing=False,
        command=lambda v: code_var.set(RATING_MAP.get(v, (1, "OBS"))[1])
    ).pack(side="left", fill="x", expand=True)

    ctk.CTkLabel(
        rating_row, textvariable=code_var,
        font=ctk.CTkFont("Segoe UI", 12, weight="bold"),
        text_color=GREEN_PRIMARY, width=50, anchor="center"
    ).pack(side="left", padx=(12, 0))

    ctk.CTkFrame(win, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")

    bottom = ctk.CTkFrame(win, fg_color=BG_HEADER, height=BOTTOM_H, corner_radius=0)
    bottom.pack(fill="x", side="bottom")
    bottom.pack_propagate(False)

    bi = ctk.CTkFrame(bottom, fg_color="transparent")
    bi.pack(fill="both", expand=True, padx=SIDE_PAD, pady=14)

    status_var = ctk.StringVar(
        value="Fill in your details and click Apply."
    )
    ctk.CTkLabel(
        bi, textvariable=status_var,
        font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT,
        anchor="w", wraplength=340
    ).pack(side="left", fill="both", expand=True)

    def on_apply():
        real_name = e_name.get().strip()
        cid       = e_cid.get().strip()
        password  = e_password.get().strip()
        rating    = rating_var.get()
        f         = config.get("sector_folder", "")

        if not all([real_name, cid, password]):
            messagebox.showwarning(
                "Missing Fields",
                "Please fill in Real Name, CID and Password.", parent=win
            )
            return

        if not f or not os.path.isdir(f):
            messagebox.showwarning(
                "No Folder",
                "Please browse to your sector file folder first.", parent=win
            )
            return

        apply_btn.configure(state="disabled", text="Applying...")
        status_var.set("Applying profile to all .prf files...")
        win.update()

        try:
            count = apply_configuration(f, real_name, cid, password, rating)
            status_var.set(
                f"Applied to {count} profile(s). Reload EuroScope to see changes."
            )
            apply_btn.configure(state="normal", text="Apply")
            messagebox.showinfo(
                "Done",
                f"Profile applied to {count} .prf file(s).\n\nReload EuroScope to see the changes.",
                parent=win
            )
            win.destroy()
        except Exception as e:
            status_var.set("Something went wrong. Please try again.")
            apply_btn.configure(state="normal", text="Apply")
            messagebox.showerror("Error", str(e), parent=win)

    ctk.CTkButton(
        bi, text="Cancel",
        font=ctk.CTkFont("Segoe UI", 11),
        fg_color=GREY_DIM, hover_color="#3a3a3a", text_color=WHITE,
        corner_radius=6, width=88, command=win.destroy
    ).pack(side="right", padx=(10, 0), fill="y")

    apply_btn = ctk.CTkButton(
        bi, text="Apply",
        font=ctk.CTkFont("Segoe UI", 11, weight="bold"),
        fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, text_color=WHITE,
        corner_radius=6, width=110, command=on_apply
    )
    apply_btn.pack(side="right", fill="y")

    win._refs = refs

    win.update_idletasks()
    h = win.winfo_reqheight()
    win.geometry(f"{WIN_W}x{h}")
    win.minsize(WIN_W, h)
    win.maxsize(WIN_W, h)

    def _reload_existing(new_folder):
        prf_files = [
            ff for ff in os.listdir(new_folder) if ff.lower().endswith(".prf")
        ] if os.path.isdir(new_folder) else []
        if prf_files:
            data = read_profile_from_prf(
                os.path.join(new_folder, prf_files[0])
            )
            e_name.delete(0, "end")
            e_name.insert(0, data.get("realname", ""))
            e_cid.delete(0, "end")
            e_cid.insert(0, data.get("certificate", ""))
            e_password.delete(0, "end")
            e_password.insert(0, data.get("password", ""))
            rv = int(data.get("rating", "1"))
            rl = RATING_VALUE_TO_LABEL.get(rv, RATINGS[0])
            rating_var.set(rl)
            code_var.set(RATING_MAP[rl][1])