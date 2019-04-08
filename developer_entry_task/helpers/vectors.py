import numpy as np
import rasterio
import rasterio.mask
from config import Config

def get_polygon_stats(polygon, img):
    if not isinstance(polygon, list):
        polygon = [polygon]
    
    query_mask = rasterio.features.rasterize(polygon, img.raster.shape, 0,
                                             transform=img.transform,
                                             all_touched=False)

    ndvi_masked = (np.copy(img.raster)*Config.RESAMPLE_VAL).astype('int64')
    ndvi_masked[query_mask == 0] = -276470
    return ndvi_masked

    # return_list = []
    # if stats:
    #     if 'min' in stats:
    #         return_list.append(int(np.nanmin(ndvi_masked[ndvi_masked!=-276470])))
    #     if 'max' in stats:
    #         return_list.append(int(np.nanmax(ndvi_masked[ndvi_masked!=-276470])))
    #     if 'mean' in stats:
    #         return_list.append(int(np.nanmean(ndvi_masked[ndvi_masked!=-276470])))
    #     if 'std' in stats:
    #         return_list.append(int(np.nanstd(ndvi_masked[ndvi_masked!=-276470])))
    # return return_list

def find_mins(stats_by_item):
    mins_dict = {}
    abs_min = 10**20
    the_pair = ''
    for i1,v1 in enumerate(stats_by_item):
        for i2,v2 in enumerate(stats_by_item):
            if i1 != i2:
                if len(v1)>1:
                    diff = np.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)
                else:
                    diff = abs(v1[0]-v2[0])
                if diff < abs_min:
                    abs_min = diff
                    the_pair = (i1, i2)
    return the_pair