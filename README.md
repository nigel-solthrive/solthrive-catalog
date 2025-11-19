# 🌞 SolThrive Catalog Repository  
Master index and documentation for the SolThrive Shopify product catalog — including Layer 1 data, Layer 2 SEO enhancements, and future Layer 3 specification automation.

This repo exists to organize and centralize all the technical documentation and folder structure used across the SolThrive Shopify Catalog stored in Google Drive. It will become the foundation for Layer 3 (Spec Matrix Builder), Layer 4 (Automation Engine), and future internal tools.

---

## 🔷 What This Repo Contains  
- **SolThrive Catalog Index** — a complete map of every category folder and data layer  
- **Documentation** for how Layer 1, Layer 2, and future Layer 3 work  
- **Reference structure** for automation scripts  
- **Repo home** for future SolThrive internal tooling  
- **A stable foundation** for future contributors or collaborators

---

## 🔷 Data Layer Definitions

### **Layer 1 — Raw → Clean Structured Catalog**
This includes:
- Cleaned raw product data  
- SKU normalization  
- Titles, vendor mapping, descriptions  
- Manual staging of images, datasheets, and spec references  

**Source:** Google Drive → `SolThrive_Shopify_Catalog/<Category>_Data/`

---

### **Layer 2 — SEO Layer**
This layer applies:
- SEO-friendly titles  
- Meta description templates  
- Short & long descriptions  
- Feature highlights  
- Vendor tone-mapping  
- Shopify-ready metafields  

**Source:** Python Layer 2 SEO Script (v2.6)

---

### **Layer 3 — Specification Matrix (Coming Soon)**
This will extract full product technical specifications and normalize them for:
- Shopify metafields  
- Comparison charts  
- Internal quote tools  
- Future filtering  
- Tech spec databases  

This repo will store all documentation + code structure for Layer 3.

---

## 🔷 Repository Structure (Recommended)

```
solthrive-catalog/
   ├── README.md
   ├── SolThrive_Catalog_Index.md
   ├── docs/
   │     ├── layer1_overview.md
   │     ├── layer2_overview.md
   │     └── layer3_design.md
   ├── assets/
   │     └── images (optional)
   └── scripts/ (future)
```

---

## 🔷 Connected Systems

- **Google Drive** (primary storage for catalog data)
- **Octoparse** (monthly Greentech scrapes)
- **Shopify** (e-commerce)
- **Webflow** (SolThrive website)
- **Python Automation Stack** (Layer 1 → Layer 2 → Layer 3 → Layer 4)

---

## 🔷 Future Expansion

### Layer 4 — Automation Engine  
Event-driven triggers:
- New file upload → auto-clean  
- New sitemap scrape → auto-process  
- Broken link alerts  
- Daily or weekly summary emails  

### Layer 5 — SolThrive Internal Dashboard  
A web-based tool for:
- Uploading datasets  
- Auto-running the entire pipeline  
- Exporting Shopify CSVs  
- Generating metafields  
- Viewing errors, diffs, and spec reports  

---

This repo is the foundation for SolThrive’s long-term catalog infrastructure.  
As the business grows, this documentation and structure will grow with it.
