# 🌲 Victorian Fuel Hazard Mapping & Field Verification

**Independent GIS & Remote Sensing Portfolio Project — 2026**

An independent project exploring how remote sensing, GIS, mobile field data collection and future GeoAI could be combined into an iterative workflow for assessing relative fuel-hazard patterns across a Victorian study area.

> **Important:** This is an independent portfolio project and a relative modelling/field-verification prototype. It is not an operational Victorian Government hazard assessment or a field-validated fire-risk product.

---

## 🎯 Project Objective

The objective is to develop an end-to-end geospatial workflow that connects:

**Remote Sensing → GIS Analysis → Relative Fuel Hazard → Field Verification → Model Evaluation → Future GeoAI**

The project focuses on developing a practical workflow rather than producing an operational fire-danger assessment.

---

## 🛰️ Stage 1 — Relative Fuel Hazard Mapping

The first stage integrates multiple spatial datasets, including:

* Sentinel-1 SAR
* Sentinel-2 optical imagery
* Vegetation and moisture indicators
* DEM-derived terrain variables
* Fire history
* Time Since Last Burnt (TSLB)
* Fuel groups
* Fire Management Zones (FMZ)

Using **Python and QGIS**, these datasets were combined to produce a relative fuel-hazard proxy map.

### Example output

![Relative Fuel Hazard Map](images/Relative%20Fuel%20Hazard%20Map.png)

The relative hazard classification was divided into:

* Low
* Moderate
* High

Zonal statistics were then used to examine the distribution of higher relative hazard across management zones.

---

## 📊 Example Result

Within the study area, approximately:

* **69.6%** of valid mapped pixels within the Bushfire Moderation Zone (BMZ) were classified as high relative hazard.
* **27.7%** within the Landscape Management Zone (LMZ) were classified as high relative hazard.

These values are **relative modelling outputs**, not field-validated hazard assessments.

---

## 📱 Stage 2 — QField Field Verification

The second stage extends the desktop GIS workflow into a mobile field-verification workflow using **QField**.

The field form is designed to separate:

### GIS-derived information

* Relative hazard score
* Hazard class
* Fuel group
* TSLB
* Last burnt
* FMZ
* PLM

### Field observations

* Observed fuel type
* Observed fuel condition
* Surface fuel continuity
* Understorey density
* Recent disturbance
* Field hazard assessment
* Photographs
* Comments

![QField Form](images/qfield-form.png)

The purpose is to create a structured dataset that can later be used to compare spatial predictions with field observations.

---

## 🔄 Proposed Feedback Loop

The longer-term concept is:

**Remote Sensing**

↓

**GIS / Relative Hazard Model**

↓

**QField Field Verification**

↓

**Field Observations**

↓

**Model Evaluation**

↓

**Future Deep Learning / GeoAI**

↓

**Updated Spatial Model**

↓

**Further Field Verification**

This creates a potential feedback loop between remote sensing, GIS, field data and machine learning.

---

## 🛠️ Technologies

**GIS & Remote Sensing**

* QGIS
* QField
* Sentinel-1
* Sentinel-2
* Google Earth Engine
* Raster analysis
* Spatial analysis
* Zonal statistics

**Programming & Data Science**

* Python
* GeoPandas
* Raster processing
* Machine learning / deep learning concepts

**Data**

* Fire history
* Time Since Last Burnt
* Fuel groups
* Fire Management Zones
* Terrain / DEM
* Vegetation and moisture indicators

---

## 🚧 Current Status

### Completed

* [x] Remote-sensing and GIS preprocessing
* [x] Relative fuel-hazard modelling
* [x] Low / Moderate / High classification
* [x] FMZ zonal analysis
* [x] QField field-verification prototype

### Future work

* [ ] Field data collection
* [ ] Compare model predictions with field observations
* [ ] Quantitative model evaluation
* [ ] Build a field-validated training dataset
* [ ] Explore deep-learning approaches
* [ ] Iteratively refine the spatial model

---

## ⚠️ Limitations

This project is an independent portfolio project.

The relative hazard outputs are intended to demonstrate a GIS and remote-sensing workflow and should not be interpreted as an official operational bushfire hazard or prescribed-burning decision product.

Field validation has not yet been completed.

---

## 👩‍💻 Project Focus

This project demonstrates my interest in connecting:

**GIS + Remote Sensing + Python + Mobile GIS + GeoAI**

to practical environmental and geospatial problems.
