"""
SolThrive Duplicate SKU & Handle Scanner
Author: SolThrive Automations
Version: 1.1.0

Purpose:
- Downloads Layer_1 files from Google Drive (direct links in config.json)
- Normalizes data across all categories
- Ensures every row has a clean Shopify-style handle (when possible)
- Detects duplicate SKUs
- Detects duplicate Shopify handles
- Outputs clean CSV reports for Shopify import validation
"""

import os
import json
import requests
import io
import re
import pandas as pd

print("Starting SolThrive Duplicate Scanner...")
print("---------------------------------------\n")

# -------------------------------------------
# Load config.json
# -------------------------------------------
config_path = os.path.join(os.path.dirname(__file__), "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

LAYER1_PATHS = config.get("LAYER1_PATHS", {})

if not LAYER1_PATHS:
    raise ValueError("No file paths found in config.json under 'LAYER1_PATHS'.")


# -------------------------------------------
# Helper: Shopify-style handle generator
# -------------------------------------------
def generate_handle(text: str) -> str:
    """
    Generate a Shopify-style handle from a text string.
    - Lowercase
    - Replace non-alphanumeric with hyphens
    - Trim leading/trailing hyphens
    """
    text = str(text).strip().lower()
    # Replace any group of non a-z0-9 with single hyphen
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def needs_new_handle(handle_value: str) -> bool:
    """
    Determine if a handle should be replaced.
    Empty strings, NaN-like values, or 'none'/'null' are treated as missing.
    """
    if handle_value is None:
        return True
    h = str(handle_value).strip().lower()
    if h in ("", "nan", "none", "null"):
        return True
    return False


# -------------------------------------------
# Download + Load Each Layer_1 File
# -------------------------------------------
all_rows = []

for category, url in LAYER1_PATHS.items():
    try:
        print(f"[INFO] Downloading: {category}")

        # Download file from Google Drive
        response = requests.get(url)
        response.raise_for_status()

        file_bytes = io.BytesIO(response.content)

        # Load into pandas
        df = pd.read_excel(file_bytes)

        df["category"] = category  # Add category column (lowercase name)
        all_rows.append(df)

        print(f"[OK] Loaded: {category}\n")

    except Exception as e:
        print(f"[ERROR] Could not load {category}: {e}\n")

# Safety check
if not all_rows:
    raise RuntimeError("No valid Layer_1 files were loaded. Cannot continue.")


# -------------------------------------------
# Merge All Layer_1 Data
# -------------------------------------------
master = pd.concat(all_rows, ignore_index=True)


# -------------------------------------------
# Normalize Columns
# -------------------------------------------
master.columns = master.columns.str.strip().str.lower()

# Required columns for Shopify & duplicate detection
required_cols = ["sku", "handle", "category"]

for col in required_cols:
    if col not in master.columns:
        print(f"[WARN] Missing column '{col}' — creating empty column.")
        master[col] = ""

# Normalize core fields
master["sku"] = master["sku"].astype(str).str.strip()
master["handle"] = master["handle"].astype(str).str.strip().str.lower()
master["category"] = master["category"].astype(str).str.strip()

if "title" in master.columns:
    master["title"] = master["title"].astype(str).str.strip()
else:
    print("[WARN] No 'title' column found — handle generation will be limited.")


# -------------------------------------------
# Handle Generation (does NOT modify your source files)
# -------------------------------------------
master["handle_original"] = master["handle"].copy()

if "title" in master.columns:
    def _apply_handle(row):
        current_handle = row["handle"]
        if needs_new_handle(current_handle):
            return generate_handle(row.get("title", ""))
        return current_handle

    master["handle"] = master.apply(_apply_handle, axis=1)
else:
    print("[INFO] Skipping handle generation because 'title' column is missing.")


# Track changes for reporting
handle_changes = master[master["handle"] != master["handle_original"]].copy()


# -------------------------------------------
# Duplicate Detection (SKU + Handle)
# Ignore empty SKUs/handles when checking duplicates
# -------------------------------------------
valid_sku_mask = master["sku"].str.len() > 0
valid_handle_mask = master["handle"].str.len() > 0

duplicate_skus = (
    master[valid_sku_mask]
    [master[valid_sku_mask].duplicated("sku", keep=False)]
    .sort_values("sku")
)

duplicate_handles = (
    master[valid_handle_mask]
    [master[valid_handle_mask].duplicated("handle", keep=False)]
    .sort_values("handle")
)


# -------------------------------------------
# Save Reports
# -------------------------------------------
output_sku = "duplicate_skus_report.csv"
output_handle = "duplicate_handles_report.csv"
output_handle_changes = "handle_corrections_report.csv"

duplicate_skus.to_csv(output_sku, index=False)
duplicate_handles.to_csv(output_handle, index=False)
handle_changes.to_csv(output_handle_changes, index=False)

# -------------------------------------------
# Final Summary
# -------------------------------------------
print("\n---- SCAN COMPLETE ----")
print(f"Total rows scanned: {len(master)}")
print(f"Duplicate SKUs found: {len(duplicate_skus)}")
print(f"Duplicate Handles found: {len(duplicate_handles)}")
print(f"Handles auto-corrected or generated: {len(handle_changes)}\n")

print("Reports saved:")
print(f"- {output_sku}")
print(f"- {output_handle}")
print(f"- {output_handle_changes}\n")

print("SolThrive Duplicate Scanner finished successfully.")
