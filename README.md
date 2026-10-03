# 🌲 Victorian Fuel Hazard Mapping & Field Verification

**Independent GIS & Remote Sensing Portfolio Project — 2026**

An independent project exploring how remote sensing, GIS, mobile field data collection, and future GeoAI can be combined into an iterative workflow for assessing relative fuel-hazard patterns across a Victorian study area.

> **Important:** This is an independent portfolio project and a relative modelling/field-verification prototype. It is not an operational Victorian Government hazard assessment or a field-validated fire-risk product.

---

## 🎯 Project Objective

The project develops an end-to-end workflow connecting:

**Remote Sensing → GIS Analysis → Relative Fuel Hazard → Field Verification → Model Evaluation → Future GeoAI**

The main objective is to demonstrate how multiple geospatial datasets can be integrated into a reproducible GIS workflow and subsequently connected to mobile field data collection.

---

## 🗺️ Workflow Overview

```text
Source GIS & Remote Sensing Data
              │
              ▼
      AOI clipping / preprocessing
              │
              ▼
      Rasterisation & alignment
              │
              ├── Sentinel-1 (SAR / Future GeoAI)
              ├── Sentinel-2 (NDVI, NDMI, MSI)
              ├── DEM / Terrain (Future GeoAI)
              ├── Fire history & TSLB
              ├── Fuel types (BFC reclassification)
              ├── FMZ (Management Context)
              └── PLM25 (Tenure Context)
              │
              ▼
     Vegetation / Dryness / Stress Scores
              │
              ▼
       Fuel Condition Score (Optical Indices)
              │
              ▼
   Time Since Last Burnt (TSLB) Normalisation
              │
              ▼
       Relative Fuel Hazard Proxy
              │
              ▼
     FMZ & Fuel Group Interpretation
              │
              ▼
     Priority Areas for Field Verification
              │
              ▼
             QField (Mobile Data Collection)
              │
              ▼
       Field Observations vs. Model Evaluation
              │
              ▼
      Future GeoAI / Deep Learning Feedback Loop
```

---

## 🛰️ Stage 1 — Relative Fuel Hazard Mapping

Stage 1 was implemented primarily using **QGIS, Python, and Google Earth Engine (GEE)**. The purpose is to create a **relative fuel-hazard proxy**, rather than an operational bushfire hazard assessment.

### 1. Study Area & Grid Setup
* **AOI Spatial Boundary:** Custom study-area polygon.
* **Coordinate Reference System (CRS):** `EPSG:7899` — GDA2020 / Vicgrid.
* **Resolution:** 10 m common raster grid.

### 2. Required Spatial Datasets

| Dataset | Type | Purpose |
| :--- | :--- | :--- |
| **Sentinel-1** | Raster | SAR backscatter and structural information (retained for feature stack / GeoAI) |
| **Sentinel-2** | Raster | Vegetation and moisture indicators (NDVI, NDMI, MSI) |
| **DEM / Terrain** | Raster | Elevation, Slope, Aspect (retained for feature stack / GeoAI) |
| **Fire History** | Vector | Historical fire occurrence (`last_burnt`, `TSLB`) |
| **Fuel Types** | Raster/Vector | BFC fuel-group classification |
| **FMZ** | Vector/Raster | Fire Management Zone context |
| **PLM25** | Vector | Public land management context |
| **AOI** | Vector | Study-area boundary mask |

> *Note: Victorian Government source datasets are not redistributed in this repository where licensing applies. The repository documents the processing workflow for reproducibility.*

### 3. Fire History & TSLB Calculation
* **Last Burnt:** Identified the most recent recorded fire year intersecting each cell (`2003`, `2007`, `2009`, `2016`, `2019`, `2020`, `2023`, `2025`).
* **Time Since Last Burnt (TSLB):** Calculated for the 2026 analysis year as:
  $$\text{TSLB} = 2026 - \text{last\_burnt}$$
* **Normalisation:** The observed TSLB range (1–23 years) was normalised to a $0\text{--}1$ scale as a relative burn-recovery indicator.

### 4. Fuel Type Reclassification
The original BFC classes were reclassified into broader environmental fuel groups:
* **Group 0:** Excluded (non-fuel / water / urban)
* **Group 1:** Forest
* **Group 2:** Woodland
* **Group 3:** Plantation
* **Group 4:** Shrubland
* **Group 5:** Grassland
* **Group 6:** Other vegetation

### 5. Remote Sensing Feature Stack
A 9-band feature stack was generated in Google Earth Engine and aligned to the master 10 m grid:
* **Bands 1–3:** NDVI (Vegetation), NDMI (Moisture), MSI (Stress) — *used in Stage 1 fuel condition scoring*.
* **Bands 4–6:** VV, VH, VV − VH (SAR backscatter & structure) — *retained for future GeoAI*.
* **Bands 7–9:** Elevation, Slope, Aspect (Terrain) — *retained for future GeoAI*.

### 6. Component Scores & Fuel Condition
* **Vegetation Score:** Min-max normalised NDVI.
* **Dryness Score:** $1 - \text{Normalised NDMI}$.
* **Stress Score:** Min-max normalised MSI.
* **Fuel Condition Score:** Weighted combination driving the immediate condition indicator:
  $$\text{FuelConditionScore} = 0.40 \times \text{Vegetation} + 0.35 \times \text{Dryness} + 0.25 \times \text{Stress}$$

### 7. Relative Fuel Hazard Proxy & Classification
The final continuous proxy integrates fuel condition and burn history:
$$\text{RelativeFuelHazard} = 0.60 \times \text{FuelConditionNormalised} + 0.40 \times \text{TSLBScore}$$
![Relative Fuel Hazard Map](Relative%20Fuel%20Hazard%20Map.png)

The continuous proxy was classified into three relative classes for visualisation and field prioritisation:
* **Low:** $< 0.33$
* **Moderate:** $0.33\text{--}0.66$
* **High:** $\ge 0.66$

### 8. Management Context Integration (FMZ & PLM25)
Fire Management Zones (FMZ) and Public Land Management (PLM25) layers were overlaid as spatial context to evaluate hazard patterns across different management zones and tenures (e.g., assessing high-hazard concentrations within specific Bushfire Management Zones via zonal statistics).

---

## 📱 Stage 2 — QField Field Verification

The GIS outputs are packaged into a QField mobile project to decouple model predictions from ground-truthing:
* **GIS-Derived Fields:** Relative hazard score, hazard class, fuel group, TSLB, FMZ, and tenure.
* **Field Observations:** Observed fuel type, fuel condition, surface fuel continuity, understorey density, recent disturbances, photographs, and field hazard notes.

```text
GIS Prediction ──> QField Deployment ──> Site Navigation ──> Field Observation & Photos ──> Data Sync
```

---

## 🔄 Stage 3 & 4 — Evaluation & Future GeoAI

* **Model Evaluation:** Comparing predicted fuel groups and hazard classes against field observations to identify spatial error patterns and refine weights.
* **Future GeoAI:** Transitioning from heuristic rules to supervised machine learning / deep learning by using the field-validated dataset alongside the full multi-sensor feature stack (Sentinel-1, Sentinel-2, DEM, terrain, and spatial context).

---

## 📁 Main Project Outputs

```text
fuel_hazard_features_2026Q1.tif   # 9-band feature stack (NDVI, NDMI, MSI, VV, VH, SAR diff, DEM, Slope, Aspect)
fuelGroups_aligned.tif           # Reclassified fuel groups (10m grid)
last_burnt.tif                   # Last recorded fire year
TSLB_2026.tif                    # Time since last burnt
TSLB_score.tif                   # Normalised TSLB score
vegetation_score.tif             # Normalised NDVI score
dryness_score.tif                # Normalised NDMI dryness score
stress_score.tif                 # Normalised MSI stress score
fuel_condition_score.tif         # Composite fuel condition score
relative_fuelhazard_proxy.tif    # Final relative fuel hazard proxy raster
FMZ.tif                          # Rasterised Fire Management Zones
PLM25.shp                        # Public land management boundaries vector
Fuel_Hazard_Field_Verification.gpkg # QField mobile package
```

---

## 🧪 Reproducibility Workflow

1. Define study area AOI (`EPSG:7899`).
2. Download and preprocess source datasets.
3. Clip, reproject, and rasterise vector layers.
4. Align all rasters to the master 10 m grid (Nearest Neighbour for categorical data, Bilinear for continuous data).
5. Generate Sentinel-1 / Sentinel-2 feature stack via Google Earth Engine.
6. Compute component scores (Vegetation, Dryness, Stress) and composite Fuel Condition.
7. Calculate Last Burnt and Normalised TSLB.
8. Derive Relative Fuel-Hazard Proxy and apply classification thresholds.
9. Perform zonal statistics across FMZ layers.
10. Export packages for QField deployment.

---

## ⚠️ Limitations

This is an **independent portfolio project**. The relative hazard model:
* Has not yet been field-validated.
* Uses heuristic modelling assumptions and manually configured weights.
* Does not represent an official Victorian Government hazard assessment and should not be used for operational fire management decisions.
* Uses TSLB based strictly on available recorded fire history records, which may not reflect actual fine-fuel accumulation on the ground.

---

## 👩‍💻 Technology Stack

* **GIS & Remote Sensing:** QGIS, QField, Google Earth Engine, Sentinel-1 (SAR), Sentinel-2 (Optical).
* **Python Libraries:** Rasterio, GeoPandas, NumPy, PyQGIS.
* **Data Processing:** Rasterisation, spatial overlay, zonal statistics, mobile spatial synchronization.
