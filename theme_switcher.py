import os

def read_themes(settings_path):
    themes = {}
    current_theme = None
    current_file  = None

    with open(settings_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            continue

        if stripped.endswith("THEME BEGIN"):
            current_theme = stripped[:-len("THEME BEGIN")].strip()
            themes[current_theme] = {
                "prf_symbology": None,
                "prf_overrides": {},
                "files": {}
            }
            current_file = None
            continue

        if stripped.endswith("THEME END"):
            current_theme = None
            current_file  = None
            continue

        if current_theme is None:
            continue

        if stripped.startswith("ALL_PRF SYMBOLOGY"):
            themes[current_theme]["prf_symbology"] = stripped[len("ALL_PRF SYMBOLOGY"):].strip()
            continue

        if stripped.startswith("PRF:"):
            rest = stripped[len("PRF:"):]
            if " SYMBOLOGY" in rest:
                file_list_part, remainder = rest.split(" SYMBOLOGY", 1)
                sympath   = remainder.strip()
                filenames = [f.strip() for f in file_list_part.split(",") if f.strip()]
                for fname in filenames:
                    themes[current_theme]["prf_overrides"][fname] = sympath
            continue

        if stripped.endswith("BEGIN") and not stripped.endswith("THEME BEGIN"):
            current_file = stripped[:-len("BEGIN")].strip()
            themes[current_theme]["files"][current_file] = []
            continue

        if stripped.endswith("END") and not stripped.endswith("THEME END"):
            current_file = None
            continue

        if current_file is not None:
            themes[current_theme]["files"][current_file].append(stripped)

    return themes

def _patch_topsky_maps(filepath, color_lines):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.readlines()

    lookup = {}
    for entry in color_lines:
        parts = entry.split(":")
        if len(parts) >= 5 and parts[0] == "COLORDEF":
            lookup[parts[1]] = f"{parts[2]}:{parts[3]}:{parts[4]}"

    new_lines = []
    for line in content:
        stripped = line.strip()
        matched  = False
        if stripped.startswith("COLORDEF:"):
            parts = stripped.split(":")
            if len(parts) >= 5 and parts[1] in lookup:
                new_lines.append(f"COLORDEF:{parts[1]}:{lookup[parts[1]]}\n")
                matched = True
        if not matched:
            new_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def _patch_topsky_settings(filepath, color_lines):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.readlines()

    lookup = {}
    for entry in color_lines:
        if "=" in entry:
            key, value = entry.split("=", 1)
            lookup[key.strip()] = value.strip()

    new_lines = []
    for line in content:
        stripped = line.strip()
        matched  = False
        if "=" in stripped and not stripped.startswith("//"):
            key = stripped.split("=")[0].strip()
            if key in lookup:
                new_lines.append(f"{key}={lookup[key]}\n")
                matched = True
        if not matched:
            new_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def _patch_prf_symbology(root_folder, default_symbology, prf_overrides):
    prf_files = [f for f in os.listdir(root_folder) if f.lower().endswith(".prf")]
    for fname in prf_files:
        sympath = prf_overrides.get(fname, default_symbology)
        if sympath is None:
            continue
        prf_path = os.path.join(root_folder, fname)
        with open(prf_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.readlines()
        new_lines = []
        for line in content:
            if "SettingsfileSYMBOLOGY" in line:
                parts = line.split("SettingsfileSYMBOLOGY")
                new_lines.append(
                    parts[0] + "SettingsfileSYMBOLOGY\t" + sympath + "\n"
                )
            else:
                new_lines.append(line)
        with open(prf_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

def apply_theme(theme_name, themes, root_folder):
    if theme_name not in themes:
        raise ValueError(f'Theme "{theme_name}" not found in Settings.txt')

    theme = themes[theme_name]

    if bool(theme["prf_symbology"]) or bool(theme["prf_overrides"]):
        _patch_prf_symbology(
            root_folder, theme["prf_symbology"], theme["prf_overrides"]
        )

    for relative_path, color_lines in theme["files"].items():
        norm      = relative_path.replace("/", "\\").lstrip("\\")
        full_path = os.path.join(root_folder, norm)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found:\n{full_path}")

        if "TopSkyMaps" in relative_path:
            _patch_topsky_maps(full_path, color_lines)
        elif "TopSkySettings" in relative_path:
            _patch_topsky_settings(full_path, color_lines)