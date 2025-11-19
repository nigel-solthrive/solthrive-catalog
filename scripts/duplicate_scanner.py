"""
SolThrive Duplicate SKU & Handle Scanner
Author: SolThrive Automations
Version: 1.0.0

Purpose:
- Downloads Layer_1 files from Google Drive (direct links)
- Normalizes the data across all categories
- Detects duplicate SKUs
- Detects duplicate Shopify handles
- Outputs clean reports for Shopify import validation
"""

import os
import json
import requests
import io
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

        df["category"] = category  # Add category column
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

# Normalize values
master["sku"] = master["sku"].astype(str).str.strip()
master["handle"] = master["handle"].astype(str).str.strip().str.lower()
master["category"] = master["category"].astype(str).str.strip()

# -------------------------------------------
# Duplicate Detection
# -------------------------------------------
duplicate_skus = master[master.duplicated("sku", keep=False)].sort_values("sku")
duplicate_handles = master[master.duplicated("handle", keep=False)].sort_values("handle")

# -------------------------------------------
# Save Reports
# -------------------------------------------
output_sku = "duplicate_skus_report.csv"
output_handle = "duplicate_handles_report.csv"

duplicate_skus.to_csv(output_sku, index=False)
duplicate_handles.to_csv(output_handle, index=False)

# -------------------------------------------
# Final Summary
# -------------------------------------------
print("\n---- SCAN COMPLETE ----")
print(f"Total rows scanned: {len(master)}")
print(f"Duplicate SKUs found: {len(duplicate_skus)}")
print(f"Duplicate Handles found: {len(duplicate_handles)}\n")

print("Reports saved:")
print(f"- {output_sku}")
print(f"- {output_handle}\n")

print("SolThrive Duplicate Scanner finished successfully.")
