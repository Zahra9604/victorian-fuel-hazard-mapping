# ============================================================
# WHOLE-AOI FUEL HAZARD FEATURE DOWNLOAD
# Personal Google Earth Engine Authentication
#
# AOI:
#   Victorian public-land study area
#
# Output:
#   Whole AOI
#   10 m resolution
#   EPSG:7899
#   9-band Float32 GeoTIFF
#   Google Drive
#
# Bands:
#   1. NDVI
#   2. NDMI
#   3. MSI
#   4. VV
#   5. VH
#   6. VV_minus_VH
#   7. elevation
#   8. slope
#   9. aspect
# ============================================================


# ------------------------------------------------------------
# 1. IMPORTS
# ------------------------------------------------------------

import time
import pathlib

import ee
import geopandas as gpd


# ------------------------------------------------------------
# 2. SETTINGS
# ------------------------------------------------------------

# Your final AOI
INPUT_SHP = r"C:\DEECA\data\AOI\AOI.shp"

# Earth Engine export settings
DRIVE_FOLDER = "DEECA_Fuel_Hazard"

EXPORT_NAME = "fuel_hazard_features_2026Q1"

START_DATE = "2026-01-01"
END_DATE = "2026-03-31"

TARGET_CRS = "EPSG:7899"

SCALE = 10

# Maximum number of pixels allowed for the export.
# Your AOI is far below this value.
MAX_PIXELS = 1e10


# ------------------------------------------------------------
# 3. AUTHENTICATE WITH YOUR PERSONAL GOOGLE ACCOUNT
# ------------------------------------------------------------

print()
print("=" * 70)
print("GOOGLE EARTH ENGINE PERSONAL ACCOUNT AUTHENTICATION")
print("=" * 70)
print()

print("Starting Earth Engine authentication...")

# This opens the Google authentication flow the first time.
ee.Authenticate()

# Initialize Earth Engine using the authenticated personal account.
ee.Initialize(project = "earth-observation-505504")

print()
print("Earth Engine initialized successfully.")
print()


# ------------------------------------------------------------
# 4. LOAD AOI
# ------------------------------------------------------------

print("=" * 70)
print("LOADING AOI")
print("=" * 70)

gdf = gpd.read_file(INPUT_SHP)

if gdf.empty:
    raise RuntimeError(
        "AOI shapefile contains no features."
    )

if gdf.crs is None:
    raise RuntimeError(
        "AOI shapefile has no CRS."
    )

print("AOI file:")
print(INPUT_SHP)

print()
print("Original CRS:")
print(gdf.crs)

print()
print("Number of AOI features:")
print(len(gdf))


# ------------------------------------------------------------
# 5. CONVERT AOI TO WGS84 FOR EARTH ENGINE
# ------------------------------------------------------------

gdf_4326 = gdf.to_crs("EPSG:4326")

geojson = gdf_4326.__geo_interface__

roi = (
    ee.FeatureCollection(geojson)
    .geometry()
)


print()
print("AOI converted to EPSG:4326 for Earth Engine.")


# ------------------------------------------------------------
# 6. CHECK AOI SIZE
# ------------------------------------------------------------

print()
print("=" * 70)
print("AOI SIZE")
print("=" * 70)

# Calculate area in EPSG:7899
gdf_projected = gdf.to_crs(TARGET_CRS)

aoi_area_m2 = (
    gdf_projected.geometry
    .area
    .sum()
)

aoi_area_km2 = (
    aoi_area_m2 / 1_000_000
)

estimated_pixels = (
    aoi_area_m2 /
    (SCALE * SCALE)
)

print(
    f"AOI area: {aoi_area_km2:,.2f} km²"
)

print(
    f"Estimated 10 m pixels: "
    f"{estimated_pixels:,.0f}"
)

print(
    f"Maximum allowed pixels: "
    f"{MAX_PIXELS:,.0f}"
)

if estimated_pixels > MAX_PIXELS:
    raise RuntimeError(
        "AOI exceeds MAX_PIXELS setting."
    )


# ------------------------------------------------------------
# 7. SENTINEL-2 CLOUD MASK
# ------------------------------------------------------------

print()
print("=" * 70)
print("PREPARING SENTINEL-2")
print("=" * 70)


def mask_s2(image):

    scl = image.select("SCL")

    # SCL classes removed:
    #
    # 3  = Cloud shadow
    # 8  = Medium probability cloud
    # 9  = High probability cloud
    # 10 = Cirrus
    # 11 = Snow / ice

    mask = (
        scl.neq(3)
        .And(scl.neq(8))
        .And(scl.neq(9))
        .And(scl.neq(10))
        .And(scl.neq(11))
    )

    return (
        image
        .updateMask(mask)
        .divide(10000)
    )


# ------------------------------------------------------------
# 8. SENTINEL-2 COLLECTION
# ------------------------------------------------------------

s2_collection = (
    ee.ImageCollection(
        "COPERNICUS/S2_SR_HARMONIZED"
    )
    .filterBounds(roi)
    .filterDate(
        START_DATE,
        END_DATE
    )
    .filter(
        ee.Filter.lt(
            "CLOUDY_PIXEL_PERCENTAGE",
            30
        )
    )
    .map(mask_s2)
)


s2_count = (
    s2_collection
    .size()
    .getInfo()
)

print()
print(
    f"Sentinel-2 images found: {s2_count}"
)

if s2_count == 0:

    raise RuntimeError(
        "No Sentinel-2 images were found."
    )


# ------------------------------------------------------------
# 9. SENTINEL-2 MEDIAN COMPOSITE
# ------------------------------------------------------------

print(
    "Creating Sentinel-2 median composite..."
)

s2 = (
    s2_collection
    .median()
    .clip(roi)
)


# ------------------------------------------------------------
# 10. SENTINEL-2 FEATURES
# ------------------------------------------------------------

print(
    "Calculating Sentinel-2 indices..."
)


# NDVI
NDVI = (
    s2
    .normalizedDifference(
        ["B8", "B4"]
    )
    .rename("NDVI")
)


# NDMI
NDMI = (
    s2
    .normalizedDifference(
        ["B8", "B11"]
    )
    .rename("NDMI")
)


# Moisture Stress Index
MSI = (
    s2
    .select("B11")
    .divide(
        s2.select("B8")
    )
    .rename("MSI")
)


# ------------------------------------------------------------
# 11. SENTINEL-1
# ------------------------------------------------------------

print()
print("=" * 70)
print("PREPARING SENTINEL-1")
print("=" * 70)


s1_collection = (
    ee.ImageCollection(
        "COPERNICUS/S1_GRD"
    )
    .filterBounds(roi)
    .filterDate(
        START_DATE,
        END_DATE
    )
    .filter(
        ee.Filter.eq(
            "instrumentMode",
            "IW"
        )
    )
    .filter(
        ee.Filter.listContains(
            "transmitterReceiverPolarisation",
            "VV"
        )
    )
    .filter(
        ee.Filter.listContains(
            "transmitterReceiverPolarisation",
            "VH"
        )
    )
)


s1_count = (
    s1_collection
    .size()
    .getInfo()
)

print()
print(
    f"Sentinel-1 images found: {s1_count}"
)

if s1_count == 0:

    raise RuntimeError(
        "No Sentinel-1 images were found."
    )


# ------------------------------------------------------------
# 12. SENTINEL-1 MEDIAN COMPOSITE
# ------------------------------------------------------------

print(
    "Creating Sentinel-1 median composite..."
)

s1 = (
    s1_collection
    .median()
    .clip(roi)
)


# ------------------------------------------------------------
# 13. SENTINEL-1 FEATURES
# ------------------------------------------------------------

VV = (
    s1
    .select("VV")
    .rename("VV")
)


VH = (
    s1
    .select("VH")
    .rename("VH")
)


VV_minus_VH = (
    VV
    .subtract(VH)
    .rename("VV_minus_VH")
)


# ------------------------------------------------------------
# 14. DEM
# ------------------------------------------------------------

print()
print("=" * 70)
print("PREPARING DEM")
print("=" * 70)


dem = (
    ee.Image(
        "USGS/SRTMGL1_003"
    )
    .clip(roi)
)


# Elevation
elevation = (
    dem
    .rename("elevation")
)


# Slope
slope = (
    ee.Terrain
    .slope(dem)
    .rename("slope")
)


# Aspect
aspect = (
    ee.Terrain
    .aspect(dem)
    .rename("aspect")
)


# ------------------------------------------------------------
# 15. CREATE FINAL 9-BAND FEATURE STACK
# ------------------------------------------------------------

print()
print("=" * 70)
print("CREATING FINAL FEATURE STACK")
print("=" * 70)


features = (
    ee.Image.cat(
        [
            NDVI,
            NDMI,
            MSI,
            VV,
            VH,
            VV_minus_VH,
            elevation,
            slope,
            aspect
        ]
    )
    .toFloat()
    .clip(roi)
)


# ------------------------------------------------------------
# 16. CHECK BAND NAMES
# ------------------------------------------------------------

band_names = (
    features
    .bandNames()
    .getInfo()
)


print()
print("Final bands:")

for i, band in enumerate(
    band_names,
    start=1
):

    print(
        f"  Band {i}: {band}"
    )


if len(band_names) != 9:

    raise RuntimeError(
        f"Expected 9 bands, "
        f"but found {len(band_names)}."
    )


# ------------------------------------------------------------
# 17. PRINT EXPORT INFORMATION
# ------------------------------------------------------------

print()
print("=" * 70)
print("EXPORT INFORMATION")
print("=" * 70)

print()
print(f"AOI area       : {aoi_area_km2:,.2f} km²")
print(f"Resolution     : {SCALE} m")
print(f"CRS            : {TARGET_CRS}")
print(f"Bands          : {len(band_names)}")
print("Data type      : Float32")
print("Format         : GeoTIFF")
print("Destination    : Google Drive")
print(f"Drive folder   : {DRIVE_FOLDER}")
print(f"File name      : {EXPORT_NAME}.tif")

print()
print("Bands:")

for i, band in enumerate(
    band_names,
    start=1
):

    print(
        f"  {i}. {band}"
    )


# ------------------------------------------------------------
# 18. START WHOLE-AOI BATCH EXPORT
# ------------------------------------------------------------

print()
print("=" * 70)
print("STARTING EARTH ENGINE EXPORT")
print("=" * 70)

print()
print("Submitting whole-AOI export...")
print()


task = ee.batch.Export.image.toDrive(

    image=features,

    description=EXPORT_NAME,

    folder=DRIVE_FOLDER,

    fileNamePrefix=EXPORT_NAME,

    region=roi,

    scale=SCALE,

    crs=TARGET_CRS,

    maxPixels=MAX_PIXELS,

    fileFormat="GeoTIFF"
)


task.start()


# ------------------------------------------------------------
# 19. PRINT TASK ID
# ------------------------------------------------------------

task_status = task.status()

print()
print("=" * 70)
print("EXPORT TASK CREATED")
print("=" * 70)

print()
print("Description:")
print(
    task_status.get(
        "description"
    )
)

print()
print("Task ID:")
print(
    task_status.get(
        "id"
    )
)

print()
print("Initial state:")
print(
    task_status.get(
        "state"
    )
)

print()
print(
    "IMPORTANT:"
)

print(
    "The export is now running on Earth Engine."
)

print(
    "You can close this terminal."
)

print(
    "The Earth Engine task will continue."
)

print()
print(
    "The output will be placed in:"
)

print(
    f"Google Drive / "
    f"{DRIVE_FOLDER} / "
    f"{EXPORT_NAME}.tif"
)

print()
print("=" * 70)
print("SCRIPT FINISHED — EXPORT SUBMITTED")
print("=" * 70)