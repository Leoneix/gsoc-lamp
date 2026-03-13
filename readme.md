# Task Implementation for Late Antiquity Modeling Project (LAMP)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)![GeoPandas](https://img.shields.io/badge/GeoPandas-GIS-green)![Rasterio](https://img.shields.io/badge/Rasterio-Raster%20Processing-orange)![Repo Size](https://img.shields.io/github/repo-size/Leoneix/gsoc-lamp)![Last Commit](https://img.shields.io/github/last-commit/Leoneix/gsoc-lamp)![Status](https://img.shields.io/badge/GSoC-Submission-success)
Implementation of the LAMP tasks involving path prediction and viewshed analysis using geospatial data for GSoc 2026.

**More Information:** [https://humanai.foundation/gsoc/2026/proposal_LAMP.html](https://humanai.foundation/gsoc/2026/proposal_LAMP.html)

---

## Tasks Implemented

### 1. Path Identification

Predicts likely movement paths between building entrances using a least-cost path model.

#### Inputs

| File | Description |
|------|-------------|
| `DEM_Subset-Original.tif` | Terrain elevation |
| `SAR-MS.tif` | Multispectral image (vegetation estimation) |
| `Orthoimage_Subset.tif` | Orthophoto |
| `BuildingFootprints.shp` | Building polygons |
| `Marks_Brief1.shp` | Entrance points |

#### Method

1. Compute terrain slope from DEM
2. Estimate vegetation density using NDVI
3. Extract path likelihood from orthophoto
4. Rasterize building footprints as barriers
5. Build a combined cost surface
6. Compute least-cost paths using `skimage.graph.route_through_array()`

#### Output

`predicted_paths.shp` - GIS vector layer representing predicted paths between entrances.

---

### 2. Viewshed Analysis

Computes the visible terrain area from an observer point.

#### Input

`DEM_Subset-WithBuildings.tif` — DEM including terrain and building heights.

#### Method

1. Convert observer point to raster coordinates
2. Perform line-of-sight checks across the DEM
3. Mark visible cells
4. Convert visibility raster to polygons

#### Output

`viewshed.shp` — GIS vector layer of visible terrain.

---

## Dependencies

```
rasterio
geopandas
numpy
scikit-image
shapely
pyvista
```

Install:

```bash
pip install rasterio geopandas numpy scikit-image shapely pyvista
```


## Visualization
# Task Implementation Late Antiquity Modeling Project (LAMP)
Implementation of the LAMP tasks involving path prediction and viewshed analysis using geospatial data for GSoc 2026.

**More Information:** [https://humanai.foundation/gsoc/2026/proposal_LAMP.html](https://humanai.foundation/gsoc/2026/proposal_LAMP.html)

---

## Tasks Implemented

### 1. Path Identification

Predicts likely movement paths between building entrances using a least-cost path model.

#### Inputs

| File | Description |
|------|-------------|
| `DEM_Subset-Original.tif` | Terrain elevation |
| `SAR-MS.tif` | Multispectral image (vegetation estimation) |
| `Orthoimage_Subset.tif` | Orthophoto |
| `BuildingFootprints.shp` | Building polygons |
| `Marks_Brief1.shp` | Entrance points |

#### Method

1. Compute terrain slope from DEM
2. Estimate vegetation density using NDVI
3. Extract path likelihood from orthophoto
4. Rasterize building footprints as barriers
5. Build a combined cost surface
6. Compute least-cost paths using `skimage.graph.route_through_array()`

#### Output

`predicted_paths.shp` - GIS vector layer representing predicted paths between entrances.

---

### 2. Viewshed Analysis

Computes the visible terrain area from an observer point.

#### Input

`DEM_Subset-WithBuildings.tif` — DEM including terrain and building heights.

#### Method

1. Convert observer point to raster coordinates
2. Perform line-of-sight checks across the DEM
3. Mark visible cells
4. Convert visibility raster to polygons

#### Output

`viewshed.shp` — GIS vector layer of visible terrain.

---

## Dependencies

```
rasterio
geopandas
numpy
scikit-image
shapely
pyvista
```

Install:

```bash
pip install rasterio geopandas numpy scikit-image shapely pyvista
```


## Visualization
![Predicted Path (Yellow), Entrances (Red)](https://github.com/user-attachments/assets/1c43b7a7-368c-4e1b-861f-33a1f1a1a5fa)

*Predicted Path (Yellow), Entrances (Red).*

### 3D Viewshed Visualization

![3D visualization of the viewshed](https://github.com/user-attachments/assets/8827186f-9605-4ec2-99f3-060638655a24)

*3D visualization of the viewshed.*







