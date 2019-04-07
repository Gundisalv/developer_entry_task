import os

import geopandas
import numpy as np
import rasterio
import rasterio.mask
from sentinelhub import BBox

from developer_entry_task.helpers.rasters import (GetSentinelHubImages,
                                                  SentinelHubImage)


def get_ndvi(bbox, query_date, eval_script=False):
    response = GetSentinelHubImages(bbox=bbox, end_date=query_date, maxcc=1,
                                    eval_script=eval_script, save_data=True,
                                    to_nan=False)
    ndvi_array = (response.images[0][:, :, 1]-response.images[0][:, :, 0])/(
        response.images[0][:, :, 1]+response.images[0][:, :, 0])
    red_band = SentinelHubImage(
        response.images[0][:, :, 0], bbox, response.dates_list[0])
    nir_band = SentinelHubImage(
        response.images[0][:, :, 1], bbox, response.dates_list[0])

    return SentinelHubImage(ndvi_array, bbox, response.dates_list[0])


def get_statistics(query, query_date=False, eval_script=False, shp_path=False):
    if not query_date:
        query_date = query_date = '2018-09-28'
    if not eval_script:
        eval_script = 'return [B04,B08]'
    if not shp_path:
        shp_path = os.path.join(
            os.getcwd(), 'resources/polygons/land_polygons.shp')

    vectors = geopandas.read_file(shp_path)

    possible_labels = list(vectors.LAND_TYPE.unique())

    bbox = BBox(bbox=list(vectors.geometry.total_bounds),
                crs=vectors.crs['init'])

    ndvi_img = get_ndvi(bbox, query_date, eval_script)
    try:
        if isinstance(query, int):
            polygon = vectors[query:query+1].geometry.values[0]
            query_mask = rasterio.features.rasterize([polygon],
                                                     ndvi_img.raster.shape, 0,
                                                     transform=ndvi_img.transform,
                                                     all_touched=False)
        elif all([isinstance(query, str), query in possible_labels]):
            land_type = vectors.loc[vectors['LAND_TYPE'] == query]
            polygon = land_type.dissolve(by='LAND_TYPE').geometry.values[0]
            query_mask = rasterio.features.rasterize(polygon,
                                                     ndvi_img.raster.shape, 0,
                                                     transform=ndvi_img.transform,
                                                     all_touched=False)
    except:
        print('Query does not match with any ID nor LAND_TYPE')
        exit(0)

    ndvi_masked = np.copy(ndvi_img.raster)
    ndvi_masked[query_mask == 0] = np.nan
    ndvi_masked = SentinelHubImage(ndvi_masked, bbox)
    ndvi_masked._run_stats()
    return ndvi_masked.min, ndvi_masked.max, ndvi_masked.mean, ndvi_masked.std


def get_statistics(query, query_date=False, eval_script=False, shp_path=False):
    if not query_date:
        query_date = query_date = '2018-09-28'
    if not eval_script:
        eval_script = 'return [B04,B08]'
    if not shp_path:
        shp_path = os.path.join(
            os.getcwd(), 'resources/polygons/land_polygons.shp')

    vectors = geopandas.read_file(shp_path)

    possible_labels = list(vectors.LAND_TYPE.unique())

    bbox = BBox(bbox=list(vectors.geometry.total_bounds),
                crs=vectors.crs['init'])

    ndvi_img = get_ndvi(bbox, query_date, eval_script)
    try:
        if isinstance(query, int):
            polygon = vectors[query:query+1].geometry.values[0]
            query_mask = rasterio.features.rasterize([polygon],
                                                     ndvi_img.raster.shape, 0,
                                                     transform=ndvi_img.transform,
                                                     all_touched=False)
        elif all([isinstance(query, str), query in possible_labels]):
            land_type = vectors.loc[vectors['LAND_TYPE'] == query]
            polygon = land_type.dissolve(by='LAND_TYPE').geometry.values[0]
            query_mask = rasterio.features.rasterize(polygon,
                                                     ndvi_img.raster.shape, 0,
                                                     transform=ndvi_img.transform,
                                                     all_touched=False)
    except:
        print('Query does not match with any ID nor LAND_TYPE')
        exit(0)

    ndvi_masked = np.copy(ndvi_img.raster)
    ndvi_masked[query_mask == 0] = np.nan
    ndvi_masked = SentinelHubImage(ndvi_masked, bbox)
    ndvi_masked._run_stats()
    return ndvi_masked.min, ndvi_masked.max, ndvi_masked.mean, ndvi_masked.std
