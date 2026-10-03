# 🌲 Victorian Fuel Hazard Mapping & Field Verification

**Independent GIS & Remote Sensing Portfolio Project — 2026**

An independent portfolio project exploring how **remote sensing, GIS, mobile field data collection, and future GeoAI** can be combined into an iterative workflow for assessing relative fuel-hazard patterns across a Victorian study area.

> **Important:** This is an independent portfolio project and a relative modelling/field-verification prototype. It is **not** an operational Victorian Government hazard assessment or a field-validated fire-risk product.

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
              ├── Sentinel-1
              ├── Sentinel-2
              ├── DEM / terrain
              ├── Fire history
              ├── Fuel types
              ├── FMZ
              └── PLM25
              │
              ▼
    Vegetation / Dryness / Stress
              │
              ▼
       Fuel Condition Score
              │
              ▼
       Time Since Last Burnt
              │
              ▼
   Relative Fuel Hazard Proxy
              │
              ▼
      FMZ / Fuel Group / PLM25
          interpretation
              │
              ▼
      Priority areas for
       field verification
              │
              ▼
             QField
              │
              ▼
       Field observations
              │
              ▼
       Model evaluation
              │
              ▼
      Future GeoAI / Deep Learning
```

---

# 🛰️ Stage 1 — Relative Fuel Hazard Mapping

Stage 1 was implemented primarily using:

* **QGIS**
* **Python**
* **Google Earth Engine**

The purpose was to create a **relative fuel-hazard proxy**, rather than an operational bushfire hazard assessment.

---

## 1. Study Area

A study-area polygon was defined and used as the common spatial boundary for the analysis.

The AOI was transformed to:

**EPSG:7899 — GDA2020 / Vicgrid**

The final analysis grid uses:

* **Resolution:** 10 m
* **CRS:** EPSG:7899
* **Common raster grid**
* **Common extent and alignment**

---

## 2. Spatial Datasets

| Dataset      | Type                           | Purpose                                    |
| ------------ | ------------------------------ | ------------------------------------------ |
| Sentinel-1   | Raster                         | SAR backscatter and structural information |
| Sentinel-2   | Raster                         | Vegetation and moisture indicators         |
| DEM          | Raster                         | Elevation                                  |
| Slope        | Raster                         | Terrain                                    |
| Aspect       | Raster                         | Terrain                                    |
| Fire History | Vector                         | Historical fire occurrence                 |
| Fuel Types   | Raster / vector-derived raster | Fuel-group classification                  |
| FMZ          | Vector / raster                | Fire Management Zone context               |
| PLM25        | Vector                         | Public land management context             |
| AOI          | Vector                         | Study-area boundary                        |

The Victorian Government source datasets are **not redistributed in this repository** where licensing or distribution conditions apply.

Instead, the repository documents the dataset names and processing workflow so that the analysis can be reproduced using the appropriate source datasets.

---

## 3. AOI Clipping

All relevant datasets were spatially clipped to the study area.

This was done to:

* reduce processing requirements;
* maintain a consistent study boundary;
* reduce unnecessary raster size;
* ensure that subsequent analysis uses the same spatial extent.

The AOI was retained as a vector layer and used as the spatial mask for raster processing.

---

## 4. Fire History Processing

The fire-history dataset was clipped to the AOI.

The available fire-history records included:

```text
2003
2007
2009
2016
2019
2020
2023
2025
```

The fire polygons were used to derive:

* `last_burnt`
* `TSLB`
* fire-history context for interpretation

### Last Burnt

For each raster cell, the most recent recorded fire year was identified.

```text
last_burnt = most recent fire year intersecting the cell
```

The resulting raster contains values such as:

```text
2003
2007
2009
2016
2019
2020
2023
2025
```

---

## 5. Time Since Last Burnt (TSLB)

TSLB was calculated from the most recent fire year.

For the 2026 analysis:

```text
TSLB = 2026 - last_burnt
```

QGIS Raster Calculator expression:

```text
if(
    "last_burnt@1" > 0,
    2026 - "last_burnt@1",
    -9999
)
```

This produces the number of years since the most recently recorded fire.

### TSLB Normalisation

The observed TSLB range was normalised to approximately 0–1.

For the project range of 1–23 years:

```text
("TSLB_aligned@1" - 1) / 22
```

Interpretation:

```text
0 → relatively recently burnt
1 → relatively long time since recorded burning
```

> **Important:** TSLB is a relative burn-history indicator. It does not directly measure fuel accumulation, fuel age, or fuel quantity.

---

## 6. Fuel Type Reclassification

The original fuel-type dataset contains BFC classes.

These were reclassified into broader fuel groups.

| Fuel Group | Meaning          | BFC Classes                                      |
| ---------- | ---------------- | ------------------------------------------------ |
| 0          | Excluded         | 633, 640, 700, 800, 910, 920, 930, 940, 950, 960 |
| 1          | Forest           | 110, 120, 210, 220, 230                          |
| 2          | Woodland         | 411, 421, 422, 423, 424, 431, 432, 433, 434      |
| 3          | Plantation       | 310, 321, 322, 323, 324, 330                     |
| 4          | Shrubland        | 510, 520, 531, 532, 533                          |
| 5          | Grassland        | 620, 631, 632                                    |
| 6          | Other vegetation | 610                                              |

The fuel-group raster was then:

1. clipped to the AOI;
2. reclassified;
3. assigned a NoData value outside the valid study area;
4. aligned to the common 10 m analysis grid.

---

## 7. Remote Sensing Feature Stack

A Sentinel-1 / Sentinel-2 / terrain feature stack was generated.

The final feature raster contains nine bands:

| Band | Feature   | Main Purpose                  |
| ---- | --------- | ----------------------------- |
| 1    | NDVI      | Vegetation condition          |
| 2    | NDMI      | Vegetation moisture / dryness |
| 3    | MSI       | Moisture stress               |
| 4    | VV        | SAR backscatter               |
| 5    | VH        | SAR backscatter               |
| 6    | VV − VH   | SAR structural information    |
| 7    | Elevation | Terrain                       |
| 8    | Slope     | Terrain                       |
| 9    | Aspect    | Terrain                       |

### Current Model Architecture

The current relative hazard proxy uses:

```text
NDVI
 ↓
Vegetation Score

NDMI
 ↓
Dryness Score

MSI
 ↓
Stress Score

Vegetation + Dryness + Stress
 ↓
Fuel Condition Score

Fuel Condition + TSLB
 ↓
Relative Fuel Hazard Proxy
```

The following features are currently **retained in the feature stack but are not directly included in the Stage 1 proxy formula**:

```text
VV
VH
VV − VH
Elevation
Slope
Aspect
```

These variables provide additional spatial information that could be incorporated into future machine-learning or deep-learning models.

---

## 8. Vegetation Score

NDVI was used as the primary vegetation indicator.

The NDVI values were normalised to a 0–1 relative vegetation score using min-max normalisation:

```text
VegetationScore =
    (NDVI - NDVI_min)
    /
    (NDVI_max - NDVI_min)
```

Conceptually:

```text
Low NDVI  → lower vegetation score
High NDVI → higher vegetation score
```

This score represents the relative vegetation signal within the study area.

> It should not be interpreted as a direct measurement of fuel load.

---

## 9. Dryness Score

NDMI was used as a vegetation-moisture indicator.

Because higher NDMI generally represents greater vegetation moisture, the relative dryness score was calculated as:

```text
DrynessScore =
    1 - Normalised_NDMI
```

where:

```text
Normalised_NDMI =
    (NDMI - NDMI_min)
    /
    (NDMI_max - NDMI_min)
```

Therefore:

```text
Higher NDMI → lower dryness score
Lower NDMI  → higher dryness score
```

---

## 10. Stress Score

MSI was used as the primary moisture-stress indicator.

The relative stress score was calculated using min-max normalisation:

```text
StressScore =
    (MSI - MSI_min)
    /
    (MSI_max - MSI_min)
```

Higher MSI values therefore contribute to a higher relative stress score.

---

## 11. Fuel Condition Score

The three component scores were combined into a composite fuel-condition indicator.

The weighting used was:

```text
FuelConditionScore =
    0.40 × VegetationScore
  + 0.35 × DrynessScore
  + 0.25 × StressScore
```

Therefore:

```text
Vegetation condition → 40%
Dryness              → 35%
Stress               → 25%
```

The result is a continuous relative fuel-condition score.

> These weights are modelling choices for this portfolio prototype. They are not official Victorian Government fuel-hazard weights.

---

## 12. Raster Alignment

Before combining the datasets, the raster layers were aligned to a common master grid.

The master grid was based on the project feature raster:

```text
CRS:        EPSG:7899
Resolution: 10 m
```

Each raster was transformed to the same:

* CRS
* pixel size
* extent
* width
* height
* affine transform
* pixel alignment

Categorical datasets such as fuel groups and last-burnt classes were resampled using:

```text
Nearest Neighbour
```

Continuous datasets such as vegetation and moisture indicators were resampled using:

```text
Bilinear
```

This ensured that each raster cell represented the same geographic location across the analysis.

---

## 13. Relative Fuel Hazard Proxy

The final proxy combines:

* **Fuel Condition**
* **Time Since Last Burnt**

First, the fuel-condition score was normalised using the observed project range:

```text
Minimum = 0.22280053794384
Maximum = 0.8565052151679993
```

The normalised fuel-condition score was:

```text
FuelConditionNormalised =
    (FuelConditionScore - 0.22280053794384)
    /
    (0.8565052151679993 - 0.22280053794384)
```

The relative hazard proxy was then calculated as:

```text
RelativeFuelHazard =
    0.60 × FuelConditionNormalised
  + 0.40 × TSLBScore
```

This produces a continuous relative score between approximately:

```text
0 → lower relative hazard proxy
1 → higher relative hazard proxy
```

The model therefore gives greater weight to current fuel-condition indicators while also accounting for time since the most recent recorded fire.

> This is a portfolio modelling framework. The resulting score should not be interpreted as an official bushfire risk or hazard measure.

---

## 14. Relative Hazard Classification

The continuous proxy was converted into three relative classes:

| Score     | Class    |
| --------- | -------- |
| < 0.33    | Low      |
| 0.33–0.66 | Moderate |
| ≥ 0.66    | High     |

These classes are used for:

* visualisation;
* spatial interpretation;
* field-verification prioritisation.

They do **not** represent official bushfire hazard categories.

---

## 15. FMZ Integration

Fire Management Zones (FMZ) were incorporated after the relative hazard surface had been created.

The FMZ dataset was:

1. clipped to the AOI;
2. rasterised at 10 m;
3. aligned to the master raster grid.

The FMZ raster was then overlaid with the relative hazard proxy.

This allows the analysis to investigate questions such as:

```text
Where are higher relative hazard patterns occurring?

Which fuel groups do these areas occur in?

Which FMZs contain higher relative hazard areas?

Are higher relative hazard areas concentrated in particular
parts of a management zone?
```

The FMZ layer is therefore used as **management context**, rather than as a direct component of the hazard score.

---

## 16. Fuel Group Interpretation

Fuel groups were overlaid with the relative hazard proxy to examine the vegetation/fuel context of higher-score areas.

For example:

```text
Relative Hazard
      +
Fuel Group
      ↓
Forest
Woodland
Plantation
Shrubland
Grassland
Other vegetation
```

This helps distinguish a high relative score occurring in:

* forest;
* woodland;
* plantation;
* shrubland;
* grassland.

Rather than treating all pixels as the same fuel environment.

---

## 17. PLM25 Integration

The PLM25 dataset was incorporated as an additional land-management context layer.

PLM25 is **not used as a direct predictor in the current relative hazard formula**.

Instead, it can be used to investigate:

```text
Relative hazard
       +
Fuel group
       +
FMZ
       +
Public land / management context
```

This provides additional context for selecting areas for future field verification.

---

## 18. Zonal Analysis

Zonal statistics were used to summarise relative hazard within FMZ polygons.

For example:

```text
FMZ
 │
 ├── Number of valid pixels
 ├── Mean relative hazard
 ├── Maximum relative hazard
 ├── High relative-hazard pixel count
 └── High relative-hazard percentage
```

For the current study area, the prototype produced approximately:

* **69.6%** of valid BMZ pixels classified as high relative hazard.
* **27.7%** of valid LMZ pixels classified as high relative hazard.

These are **model-derived statistics for this study area and dataset**, not operational estimates of bushfire risk.

---

## 19. Field Verification Priority

The relative hazard map is then used to identify locations for potential field verification.

The purpose is **not to assume that the model is correct**.

Instead:

```text
Predicted relative hazard
          ↓
Select verification locations
          ↓
Observe actual site conditions
          ↓
Record observations in QField
          ↓
Compare prediction vs observation
```

This creates the foundation for evaluating and improving the model.

---

# 📱 Stage 2 — QField Field Verification

The Stage 1 output is connected to a **QField** project.

The QField form separates **GIS-derived information** from **field observations**.

### GIS-derived Information

These values are populated from the GIS analysis:

* Relative hazard score
* Hazard class
* Fuel group
* TSLB
* Last burnt
* FMZ
* PLM25 information

### Field Observations

The field worker records:

* Observed fuel type
* Observed fuel condition
* Surface fuel continuity
* Understorey density
* Recent disturbance
* Field hazard assessment
* Photographs
* Comments

### QField Workflow

```text
GIS prediction
      ↓
QField project
      ↓
Navigate to verification location
      ↓
Review predicted conditions
      ↓
Record field observations
      ↓
Take photographs
      ↓
Submit observation
      ↓
Synchronise data
```

The resulting dataset provides a structured way to compare model predictions with future field observations.

---

# 🔄 Stage 3 — Future Model Evaluation

Once field observations become available, the dataset can be used to compare:

```text
Predicted condition
        vs
Observed condition
```

Potential evaluation measures include:

* agreement between predicted and observed fuel groups;
* agreement between relative hazard classes;
* spatial error patterns;
* confusion matrices for categorical predictions;
* correlation between continuous model scores and field observations.

The evaluation stage is intended to identify where the initial relative model agrees with field observations and where further refinement may be required.

---

# 🤖 Stage 4 — Future GeoAI

The field-verified observations could eventually become a training dataset for a supervised machine-learning or deep-learning workflow.

Potential input features include:

### Sentinel-2

* NDVI
* NDMI
* MSI
* spectral bands

### Sentinel-1

* VV
* VH
* VV/VH-derived features

### Terrain

* DEM
* slope
* aspect

### Spatial Context

* Fuel groups
* Fire history
* TSLB
* FMZ
* Other relevant spatial variables

The conceptual workflow would become:

```text
Remote Sensing
      ↓
Feature Stack
      ↓
Initial Relative Model
      ↓
QField Field Verification
      ↓
Field-validated Dataset
      ↓
Machine Learning / Deep Learning
      ↓
Updated Spatial Prediction
      ↓
Further Field Verification
```

This creates an iterative:

**GIS → Field Data → GeoAI → GIS**

feedback loop.

---

# 📁 Main Project Outputs

The project currently produces the following major outputs:

```text
fuel_hazard_features_2026Q1.tif
│
├── NDVI
├── NDMI
├── MSI
├── VV
├── VH
├── VV_minus_VH
├── elevation
├── slope
└── aspect

fuelGroups_aligned.tif

last_burnt.tif

TSLB_2026.tif

TSLB_score.tif

vegetation_score.tif

dryness_score.tif

stress_score.tif

fuel_condition_score.tif

relative_fuelhazard_proxy.tif

FMZ.tif

PLM25.shp

Fuel_Hazard_Field_Verification.gpkg
```

---

# 🧪 Reproducibility

The repository documents the processing workflow rather than uploading all source government datasets.

The processing sequence is:

```text
1. Define AOI
2. Download / prepare source datasets
3. Clip datasets to AOI
4. Reproject where required
5. Rasterise vector datasets
6. Align all rasters to the master 10 m grid
7. Generate Sentinel-1 / Sentinel-2 feature stack
8. Calculate vegetation score
9. Calculate dryness score
10. Calculate stress score
11. Calculate fuel condition score
12. Calculate last burnt
13. Calculate TSLB
14. Normalise TSLB
15. Calculate relative fuel-hazard proxy
16. Classify Low / Moderate / High
17. Overlay FMZ and fuel groups
18. Perform zonal statistics
19. Identify potential field-verification areas
20. Prepare QField project
```

---

# ⚠️ Limitations

This is an **independent portfolio project**.

The relative hazard model:

* has not yet been field validated;
* uses modelling assumptions and manually selected weights;
* is intended to demonstrate a geospatial workflow;
* does not represent an official Victorian Government hazard assessment;
* should not be used for operational fire management or prescribed-burning decisions.

The TSLB layer represents **time since the most recent recorded fire in the available fire-history dataset**.

It does not necessarily represent the actual age, quantity, structure, or continuity of fuel at every location.

The field-verification stage is designed to provide future observations that can be used to evaluate these assumptions.

---

# 👩‍💻 Technologies

### GIS & Remote Sensing

* **QGIS**
* **QField**
* **Google Earth Engine**
* **Sentinel-1**
* **Sentinel-2**
* Raster analysis
* Spatial analysis
* Zonal statistics

### Programming

* **Python**
* **Rasterio**
* **GeoPandas**
* **NumPy**
* **PyQGIS**
* Machine learning / deep-learning concepts

### Data Processing

* Rasterisation
* Reprojection
* Raster alignment
* Raster Calculator
* Spatial overlay
* Zonal statistics
* Mobile GIS data collection

---

# 🌲 Project Focus

This project demonstrates how:

**GIS + Remote Sensing + Python + Mobile GIS + GeoAI**

can be connected into a reproducible workflow for environmental and land-management applications.

The key concept is not simply producing a map, but creating a workflow where:

> **spatial predictions can be taken into the field, compared with observations, and eventually used to improve the next generation of the model.**

---

# 📌 Project Status

| Stage                                 | Status          |
| ------------------------------------- | --------------- |
| AOI preparation                       | ✅ Complete      |
| Spatial preprocessing                 | ✅ Complete      |
| Sentinel-1 / Sentinel-2 feature stack | ✅ Complete      |
| Fuel-group classification             | ✅ Complete      |
| Fire-history processing               | ✅ Complete      |
| TSLB calculation                      | ✅ Complete      |
| Relative fuel-condition modelling     | ✅ Complete      |
| Relative hazard proxy                 | ✅ Complete      |
| FMZ / PLM25 integration               | ✅ Complete      |
| Zonal analysis                        | ✅ Complete      |
| QField workflow                       | ✅ Complete      |
| Field observations                    | 🔄 Future stage |
| Model validation                      | 🔄 Future stage |
| GeoAI / deep-learning model           | 🔄 Future stage |

---

# 📬 Project Scope

This project is intended as a **technical portfolio demonstration** of:

* GIS workflow design
* Remote sensing data integration
* Raster processing
* Spatial modelling
* Python-based geospatial processing
* Mobile GIS field-data collection
* Reproducible analysis
* GeoAI workflow design

It demonstrates a workflow architecture rather than an operational bushfire-management system.
