# SolThrive Automations — Scripts Overview

This folder contains automation tools for the SolThrive Catalog pipeline.

---

## 1. `duplicate_scanner.py`

### Purpose
Scans all Layer_1 category files for:
- Duplicate SKUs  
- Duplicate Shopify Handles  
- Cross-category collisions  

This prevents Shopify import failures and ensures each product exists as a single canonical listing.

### Inputs
- Layer_1 Excel files located in Google Drive  
- File paths must be updated in `LAYER1_PATHS`

### Outputs
- `duplicate_skus_report.csv`
- `duplicate_handles_report.csv`
- Console summary

### Coming Enhancements
- Auto-load file paths from `config.json`
- Shopify handle generator
- Layer_1 → Master_Catalog builder
- Cross-layer alignment (Layer 2 + Layer 3)

---

## Future Scripts (Planned)
- `spec_matrix_builder.py` (Layer 3)
- `image_datasheet_validator.py`
- `greentech_scrape_normalizer.py`
- `shopify_import_validator.py`
