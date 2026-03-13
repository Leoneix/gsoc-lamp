import rasterio
import geopandas as gpd
import numpy as np
from skimage.graph import route_through_array
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from rasterio.features import rasterize


with rasterio.open("Task_1/Orthoimage_Subset.tif") as src:
    print("Band count:", src.count)