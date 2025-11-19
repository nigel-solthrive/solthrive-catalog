# Layer 3 — Specification Matrix Builder (Design Blueprint)

Layer 3 extracts **full technical specifications** for each product and converts them into normalized metafields that Shopify can store and display.

This layer enables:
- Product comparison features  
- Filterable specs (Voc, Isc, power rating, etc.)  
- Technical details on product pages  
- Future quote-tool integrations  
- Internal spec database creation  

---

## 🔹 Goals
- Read product spec sheets  
- Parse structured and semi-structured spec tables  
- Normalize technical terminology  
- Output a clean, unified spec model for Shopify metafields  

---

## 🔹 Output Format

Example Shopify metafield structure for Solar Panels:

```
specs:stc_power
specs:ptc_power
specs:voc
specs:isc
specs:module_efficiency
specs:dimensions_length
specs:dimensions_width
specs:dimensions_depth
specs:weight
```

This system will eventually support every category.

---

## 🔹 Input Requirements
- Clean Layer 1 data  
- Vendor datasheet PDFs  
- Extracted/cleaned tables (future automation)  
- Normalized data dictionaries  

---

## 🔹 Automation Flow
```
Layer 1 (clean data)
    ↓
Layer 2 (SEO + metafields)
    ↓
Layer 3 (spec extraction + normalization)
    ↓
Shopify Import (Products + Metafields)
    ↓
Live Store
```

---

## 🔹 Future Enhancements (Layer 4+)
- Auto-download datasheets  
- OCR and table extraction  
- Vendor-specific parsing logic  
- Daily error reporting  
- Versioned spec history  

Layer 3 is the **technical heart** of SolThrive’s future automation engine.

