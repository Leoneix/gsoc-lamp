import rasterio
import numpy as np
import geopandas as gpd
import math

from rasterio.transform import rowcol
from rasterio.features import shapes
from shapely.geometry import shape

# Load DEM
with rasterio.open("Task_1/DEM_Subset-WithBuildings.tif") as src:
    dem = src.read(1)
    transform = src.transform
    dem_crs = src.crs

rows, cols = dem.shape
print("DEM shape:", dem.shape)

# Load observer points
points = gpd.read_file("Task_1/Marks_Brief1.shp")

# explode MultiPoint → Point
points = points.explode(index_parts=False)

# reproject points to DEM CRS (CRITICAL)
points = points.to_crs(dem_crs)

observer = points.geometry.iloc[0]
print("Observer world coords:", observer.x, observer.y)

# convert world → raster pixel
row, col = rowcol(transform, observer.x, observer.y)

print("Observer pixel:", row, col)

if not (0 <= row < rows and 0 <= col < cols):
    raise ValueError("Observer pixel outside DEM bounds")

# Initialize viewshed
viewshed = np.zeros_like(dem)
obs_height = dem[row, col] + 1.7

# Viewshed calculation
for r in range(rows):
    for c in range(cols):

        dr = r - row
        dc = c - col
        dist = math.sqrt(dr**2 + dc**2)

        if dist == 0:
            viewshed[r, c] = 1
            continue

        slope = (dem[r, c] - obs_height) / dist
        visible = True

        for i in range(1, int(dist)):

            rr = row + int(dr * i / dist)
            cc = col + int(dc * i / dist)

            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                continue

            h = dem[rr, cc]
            d = math.sqrt((rr-row)**2 + (cc-col)**2)

            if (h - obs_height) / d > slope:
                visible = False
                break

        if visible:
            viewshed[r, c] = 1

print("Viewshed computed")

# Raster to Vector
results = []
for geom, val in shapes(viewshed.astype(np.int16), transform=transform):
    if val == 1:
        results.append({"geometry": shape(geom)})

gdf = gpd.GeoDataFrame(results, crs=dem_crs)

gdf.to_file("viewshed.shp")
print("Saved viewshed.shp")

import pyvista as pv
import numpy as np

x = np.arange(dem.shape[1])
y = np.arange(dem.shape[0])

xx, yy = np.meshgrid(x, y)

grid = pv.StructuredGrid(xx, yy, dem)

plotter = pv.Plotter()
plotter.add_mesh(grid, cmap="terrain")
plotter.show()