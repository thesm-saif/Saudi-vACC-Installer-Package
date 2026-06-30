import os
from constants import RATING_MAP

ALLOWED_KEYS = {"realname", "certificate", "password", "rating"}

def read_profile_from_prf(prf_path):
    result = {}
    try:
        with open(prf_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("LastSession"):
                    parts = stripped.split(None, 2)
                    if len(parts) == 3 and parts[1] in ALLOWED_KEYS:
                        result[parts[1]] = parts[2]
    except Exception:
        pass
    return result

def apply_configuration(root_folder, real_name, cid, password, rating_label):
    if not os.path.isdir(root_folder):
        raise FileNotFoundError(f"Sector file folder not found:\n{root_folder}")

    prf_files = [f for f in os.listdir(root_folder) if f.lower().endswith(".prf")]

    if not prf_files:
        raise FileNotFoundError(f"No .prf files found in:\n{root_folder}")

    rating_value = str(RATING_MAP.get(rating_label, (1, "OBS"))[0])

    fields = {
        "realname":    real_name,
        "certificate": cid,
        "password":    password,
        "rating":      rating_value,
    }

    patched = 0

    for fname in prf_files:
        prf_path = os.path.join(root_folder, fname)

        try:
            with open(prf_path, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
        except Exception:
            continue

        if raw and not raw.endswith("\n"):
            raw += "\n"

        lines = raw.splitlines(keepends=True)
        new_lines   = []
        seen_keys   = set()

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("LastSession"):
                parts = stripped.split(None, 2)
                if len(parts) >= 2:
                    key = parts[1]

                    if key in ALLOWED_KEYS:
                        if key not in seen_keys:
                            new_lines.append(
                                f"LastSession\t{key}\t{fields[key]}\n"
                            )
                            seen_keys.add(key)
                        continue

            new_lines.append(line)
        
        for key, value in fields.items():
            if key not in seen_keys:
                new_lines.append(f"LastSession\t{key}\t{value}\n")

        try:
            with open(prf_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except Exception:
            continue

        patched += 1

    return patched