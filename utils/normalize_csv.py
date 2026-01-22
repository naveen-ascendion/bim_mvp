import csv
import os

def normalize_csv(raw_path: str, clean_path: str):
    if not os.path.exists(raw_path):
        raise FileNotFoundError(raw_path)

    with open(raw_path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        raise ValueError("Empty CSV")

    header = rows[0]
    fixed_rows = []
    current_row = []

    for row in rows[1:]:
        if len(row) == len(header):
            if current_row:
                fixed_rows.append(current_row)
                current_row = []
            fixed_rows.append(row)
        else:
            if not current_row:
                current_row = row
            else:
                current_row[-1] += " " + " ".join(row)

    if current_row:
        fixed_rows.append(current_row)

    dirpath = os.path.dirname(clean_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(clean_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(fixed_rows)

def normalize_if_needed(raw_path: str, clean_path: str):
    if not os.path.exists(clean_path):
        normalize_csv(raw_path, clean_path)
        return

    raw_mtime = os.path.getmtime(raw_path)
    clean_mtime = os.path.getmtime(clean_path)

    if raw_mtime > clean_mtime:
        normalize_csv(raw_path, clean_path)