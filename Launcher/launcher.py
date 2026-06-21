import customtkinter as ctk
from PIL import Image
import os
import sys
import subprocess

def get_app_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

APP_FOLDER = get_app_folder()
ROOT_FOLDER = APP_FOLDER

FEATURES = [
    {
        "name": "Theme Switcher",
        "description": "Switch your EuroScope colour theme",
        "folder": os.path.join(ROOT_FOLDER, "Features", "Theme Switcher", "Releases", "v1.0.0"),
        "exe": "Theme Switcher.exe",
        "icon": "app.png"
    },
]

GREEN_PRIMARY   = "#3E8F26"
GREEN_HOVER     = "#2d6b1c"
GREEN_SECONDARY = "#7EBF4A"
GOLD            = "#F4B223"
WHITE           = "#FFFFFF"
BG_DARK         = "#1A1A1A"
BG_CARD         = "#232323"
BG_CARD_HOVER   = "#2a2a2a"
BG_HEADER       = "#0f0f0f"
GREY_TEXT       = "#666666"
GREY_DIM        = "#2a2a2a"
BORDER_DEFAULT  = "#2a2a2a"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class LauncherApp:
    def __init__(self, root):
        self.root = root
        self._refs = []

        root.title("Saudi vACC - Package Installer")
        root.resizable(False, False)
        root.configure(fg_color=BG_DARK)

        ico_path = os.path.join(APP_FOLDER, "app.ico")
        try:
            root.iconbitmap(ico_path)
        except Exception:
            pass

        try:
            from PIL import ImageTk
            png_path = os.path.join(APP_FOLDER, "app.png")
            ico_img = ImageTk.PhotoImage(Image.open(png_path).resize((32, 32)))
            root.iconphoto(True, ico_img)
            self._refs.append(ico_img)
        except Exception:
            pass

        win_w = 520
        win_h = 96 + 24 + (len(FEATURES) * 80) + 60
        root.geometry(f"{win_w}x{win_h}")

        self._build_header()
        self._build_feature_list()

    def _build_header(self):
        ctk.CTkFrame(self.root, height=3, fg_color=GOLD, corner_radius=0).pack(fill="x")

        header = ctk.CTkFrame(self.root, fg_color=BG_HEADER, height=93, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.place(relx=0.0, rely=0.5, anchor="w", x=24)

        try:
            png_path = os.path.join(APP_FOLDER, "app.png")
            logo_img = ctk.CTkImage(Image.open(png_path), size=(70, 70))
            ctk.CTkLabel(left, image=logo_img, text="").pack(side="left")
            self._refs.append(logo_img)
        except Exception:
            pass

        ctk.CTkLabel(
            header, text="Package Installer",
            font=ctk.CTkFont("Segoe UI", 24, weight="bold"), text_color=WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            header, text="© 2026 VATSIM Saudi Arabia",
            font=ctk.CTkFont("Segoe UI", 9), text_color=GREY_TEXT
        ).place(relx=1.0, rely=0.5, anchor="e", x=-24)

        ctk.CTkFrame(self.root, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")

    def _build_feature_list(self):
        ctk.CTkLabel(
            self.root, text="SELECT A TOOL",
            font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT
        ).pack(anchor="w", padx=24, pady=(20, 10))

        list_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=24)

        for feature in FEATURES:
            self._build_feature_card(list_frame, feature)

    def _build_feature_card(self, parent, feature):
        card = ctk.CTkFrame(
            parent, fg_color=BG_CARD, corner_radius=10,
            border_width=1, border_color=BORDER_DEFAULT, height=68
        )
        card.pack(fill="x", pady=6)
        card.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=10)

        icon_path = os.path.join(feature["folder"], feature.get("icon", "app.png"))
        if os.path.exists(icon_path):
            try:
                icon_img = ctk.CTkImage(Image.open(icon_path), size=(40, 40))
                ctk.CTkLabel(inner, image=icon_img, text="").pack(side="left", padx=(0, 14))
                self._refs.append(icon_img)
            except Exception:
                pass

        text_block = ctk.CTkFrame(inner, fg_color="transparent")
        text_block.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            text_block, text=feature["name"],
            font=ctk.CTkFont("Segoe UI", 13, weight="bold"), text_color=WHITE, anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_block, text=feature["description"],
            font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        open_btn = ctk.CTkButton(
            inner, text="Open",
            font=ctk.CTkFont("Segoe UI", 11, weight="bold"),
            fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, text_color=WHITE,
            corner_radius=6, width=80, height=34
        )
        open_btn.configure(command=lambda f=feature, b=open_btn: self._launch_feature(f, b))
        open_btn.pack(side="right")

        def on_enter(e):
            card.configure(fg_color=BG_CARD_HOVER)

        def on_leave(e):
            card.configure(fg_color=BG_CARD)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    def _launch_feature(self, feature, button):
        exe_path = os.path.join(feature["folder"], feature["exe"])

        if not os.path.exists(exe_path):
            import tkinter.messagebox as mb
            mb.showerror(
                "Not Found",
                f'Could not find:\n{exe_path}\n\nPlease contact support or try reinstalling the package.'
            )
            return

        button.configure(text="Opening...", state="disabled")
        self.root.update()

        subprocess.Popen([exe_path], cwd=feature["folder"])

        self.root.after(700, self._fade_and_close)

    def _fade_and_close(self):
        try:
            alpha = self.root.attributes("-alpha")
            if alpha > 0.05:
                self.root.attributes("-alpha", alpha - 0.08)
                self.root.after(15, self._fade_and_close)
            else:
                self.root.destroy()
        except Exception:
            self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = LauncherApp(root)
    root.mainloop()