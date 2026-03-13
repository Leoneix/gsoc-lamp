import numpy as np
import rasterio
import geopandas as gpd
import cv2
from shapely.geometry import LineString
from rasterio.warp import reproject, Resampling
from rasterio.features import rasterize
from skimage.graph import route_through_array

DATA_PATH = "Task_1/"

# ------------------------------------------------
# Load DEM (reference raster)
# ------------------------------------------------

with rasterio.open(DATA_PATH + "DEM_Subset-Original.tif") as src:
    dem = src.read(1)
    dem_transform = src.transform
    dem_crs = src.crs
    dem_shape = dem.shape

points = gpd.read_file(DATA_PATH + "Marks_Brief1.shp")
points = points.to_crs(dem_crs)
buildings = gpd.read_file(DATA_PATH + "BuildingFootprints.shp")
buildings = buildings.to_crs(dem_crs)
# ------------------------------------------------
# Compute slope
# ------------------------------------------------

gy, gx = np.gradient(dem)

slope = np.sqrt(gx**2 + gy**2)
slope = slope / slope.max()

# ------------------------------------------------
# Load Orthophoto
# ------------------------------------------------

with rasterio.open(DATA_PATH + "Orthoimage_Subset.tif") as src:

    if src.count == 1:
        ortho = src.read(1)

    else:
        img = src.read([1,2,3])
        img = img.transpose(1,2,0)
        ortho = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    ortho_transform = src.transform
    ortho_crs = src.crs

# ------------------------------------------------
# Resample orthophoto to DEM grid
# ------------------------------------------------

ortho_resampled = np.empty(dem_shape)

reproject(
    ortho,
    ortho_resampled,
    src_transform=ortho_transform,
    src_crs=ortho_crs,
    dst_transform=dem_transform,
    dst_crs=dem_crs,
    resampling=Resampling.bilinear
)

path_prob = ortho_resampled / ortho_resampled.max()

# ------------------------------------------------
# Load multispectral raster
# ------------------------------------------------

with rasterio.open(DATA_PATH + "SAR-MS.tif") as src:

    ms = src.read()
    ms_transform = src.transform
    ms_crs = src.crs

# NDVI (example band selection)

red = ms[2]
nir = ms[3]

ndvi = (nir - red) / (nir + red + 1e-6)

vegetation = (ndvi - ndvi.min()) / (ndvi.max() - ndvi.min())

# ------------------------------------------------
# Resample vegetation to DEM grid
# ------------------------------------------------

veg_resampled = np.empty(dem_shape)

reproject(
    vegetation,
    veg_resampled,
    src_transform=ms_transform,
    src_crs=ms_crs,
    dst_transform=dem_transform,
    dst_crs=dem_crs,
    resampling=Resampling.bilinear
)

# ------------------------------------------------
# Load buildings and rasterize
# ------------------------------------------------

buildings = gpd.read_file(DATA_PATH + "BuildingFootprints.shp")
buildings = buildings.to_crs(dem_crs)

building_mask = rasterize(
    [(geom,1) for geom in buildings.geometry],
    out_shape=dem_shape,
    transform=dem_transform,
    fill=0,
    dtype="uint8"
)

building_penalty = building_mask * 100

# ------------------------------------------------
# Create cost surface
# ------------------------------------------------

cost_surface = (
    0.35 * slope +
    0.25 * veg_resampled +
    0.25 * (1 - path_prob) +
    0.15 * building_penalty
)

cost_surface = cost_surface + 1

# ------------------------------------------------
# Load entrance points
# ------------------------------------------------

points = gpd.read_file(DATA_PATH + "Marks_Brief1.shp")
points = points.to_crs(dem_crs)

from rasterio.transform import rowcol

from rasterio.transform import rowcol

def world_to_pixel(x, y, transform):

    row, col = rowcol(transform, x, y)

    return (row, col)

pixel_points = []

for geom in points.geometry:

    if geom.geom_type == "Point":

        row, col = world_to_pixel(geom.x, geom.y, dem_transform)
        pixel_points.append((row, col))

    elif geom.geom_type == "MultiPoint":

        for p in geom.geoms:

            row, col = world_to_pixel(p.x, p.y, dem_transform)
            pixel_points.append((row, col))
print("Total entrance points:", len(pixel_points))
points = gpd.read_file(DATA_PATH + "Marks_Brief1.shp")
points = points.to_crs(dem_crs)

# convert multipoints to individual points
points = points.explode(index_parts=False)
# ------------------------------------------------
# Compute least cost paths
# ------------------------------------------------

from rasterio.transform import xy

paths = []

for i in range(len(pixel_points)):
    for j in range(i + 1, len(pixel_points)):

        start = pixel_points[i]
        end = pixel_points[j]

        path, cost = route_through_array(
            cost_surface,
            start,
            end,
            fully_connected=True
        )

        coords = []

        for r, c in path:
            x, y = xy(dem_transform, r, c)
            coords.append((x, y))

        line = LineString(coords)

        paths.append({
            "geometry": line,
            "start": i,
            "end": j,
            "cost": cost
        })

print("Paths computed:", len(paths))

# ------------------------------------------------
# Save paths as GIS layer
# ------------------------------------------------

gdf = gpd.GeoDataFrame(paths, crs=dem_crs)

gdf.to_file("predicted_paths.shp")

print("Saved predicted_paths.shp")


print(points.head())
with rasterio.open(DATA_PATH + "DEM_Subset-Original.tif") as src:
    print(src.bounds)

print("Pixel points:", pixel_points)
print("DEM shape:", dem.shape)

for r,c in pixel_points:
    print(r,c)