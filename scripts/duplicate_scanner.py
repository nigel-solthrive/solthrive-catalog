"""
SolThrive Duplicate SKU & Handle Scanner
Author: SolThrive Automations
Version: 0.1.0

Purpose:
- Scans Layer_1 files across all categories
- Detects duplicate SKUs and duplicate Shopify handles
- Outputs a clean report for Shopify import validation
"""

import pandas as pd
import os

# -------------------------------------------
# CONFIG — update these with actual file paths
# -------------------------------------------
LAYER1_PATHS = {
    "BOS": "path/to/BOS_Layer_1",
    "Inverters": "path/to/Inverters_Layer_1",
    "Solar Panels": "path/to/SolarPanels_Layer_1",
    "Storage": "path/to/Storage_Layer_1",
    "Racking": "path/to/Racking_Layer_1",
    "Monitoring": "path/to/Monitoring_Layer_1",
    "EV": "path/to/EV_Layer_1",
    "Sealants": "path/to/Sealants_Layer_1",
    "PreBundled": "path/to/PreBundled_Layer_1",
}

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

# Detect duplicates
duplicate_skus = master[master.duplicated("SKU", keep=False)]
duplicate_handles = master[master.duplicated("Handle", keep=False)]

# Save reports
duplicate_skus.to_csv("duplicate_skus_report.csv", index=False)
duplicate_handles.to_csv("duplicate_handles_report.csv", index=False)

print("\n---- SCAN COMPLETE ----")
print(f"Duplicate SKUs: {len(duplicate_skus)}")
print(f"Duplicate Handles: {len(duplicate_handles)}")
print("Reports saved:")
print("- duplicate_skus_report.csv")
print("- duplicate_handles_report.csv")
