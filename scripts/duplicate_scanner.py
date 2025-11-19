"""
SolThrive Duplicate SKU & Handle Scanner
Author: SolThrive Automations
Version: 0.1.0

Purpose:
- Scans Layer_1 files across all categories
- Detects duplicate SKUs and duplicate Shopify handles
- Outputs a clean report for Shopify import validation
"""

import requests
import io

all_rows = []

for category, url in LAYER1_PATHS.items():
    try:
        print(f"[INFO] Downloading: {category}")

        response = requests.get(url)
        response.raise_for_status()

        file_bytes = io.BytesIO(response.content)

        df = pd.read_excel(file_bytes)
        df["Category"] = category
        all_rows.append(df)

        print(f"[OK] Loaded: {category}")

    except Exception as e:
        print(f"[ERROR] Could not load {category}: {e}")

# -------------------------------------------
# CONFIG — update these with actual file paths
# -------------------------------------------
import json

# Load config
config_path = os.path.join(os.path.dirname(__file__), "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

LAYER1_PATHS = config.get("LAYER1_PATHS", {})

# -------------------------------------------
# MAIN SCANNER
# -------------------------------------------
all_rows = []

for category, path in LAYER1_PATHS.items():
    try:
        df = pd.read_excel(path)
        df["Category"] = category
        all_rows.append(df)
        print(f"[OK] Loaded: {category}")
    except Exception as e:
        print(f"[ERROR] Could not load {category}: {e}")

# Combine all
master = pd.concat(all_rows, ignore_index=True)

# Normalize columns
master["SKU"] = master["SKU"].astype(str).str.strip()
master["Handle"] = master["Handle"].astype(str).str.strip().str.lower()

# Normalize column names
master.columns = master.columns.str.strip().str.lower()

# Required columns
required_cols = ["sku", "handle", "category"]

for col in required_cols:
    if col not in master.columns:
        master[col] = ""

# After normalization:
master["sku"] = master["sku"].astype(str).str.strip()
master["handle"] = master["handle"].astype(str).str.strip().str.lower()

# Detect duplicates (SKU + Handle)
duplicate_skus = master[master.duplicated("sku", keep=False)].sort_values("sku")
duplicate_handles = master[master.duplicated("handle", keep=False)].sort_values("handle")

duplicate_skus.to_csv("duplicate_skus_report.csv", index=False)
duplicate_handles.to_csv("duplicate_handles_report.csv", index=False)

print("\n---- SCAN COMPLETE ----")
print(f"Duplicate SKUs found: {len(duplicate_skus)}")
print(f"Duplicate Handles found: {len(duplicate_handles)}")
print("Reports saved as CSV files in script directory.")

# Save reports
duplicate_skus.to_csv("duplicate_skus_report.csv", index=False)
duplicate_handles.to_csv("duplicate_handles_report.csv", index=False)

print("Starting SolThrive Duplicate Scanner...")
print("---------------------------------------\n")
print("\n---- SCAN COMPLETE ----")
print(f"Duplicate SKUs: {len(duplicate_skus)}")
print(f"Duplicate Handles: {len(duplicate_handles)}")
print("Reports saved:")
print("- duplicate_skus_report.csv")
print("- duplicate_handles_report.csv")
