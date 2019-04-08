import os
from config import Config
import geopandas
import numpy as np
import rasterio
import rasterio.mask
from sentinelhub import BBox
import functools
import datetime

from developer_entry_task.helpers.rasters import (GetSentinelHubImages,
                                                  SentinelHubImage, get_ndvi)
from developer_entry_task.helpers.vectors import get_polygon_stats, find_mins



class DeveloperEntryTask():

    def __init__(self):
        t0 = datetime.datetime.now()
        query_date = query_date = '2018-09-28'
        eval_script = 'return [B04,B08]'
        shp_path = os.path.join(os.getcwd(), 'resources/polygons/land_polygons.shp')
        self.vectors = geopandas.read_file(shp_path)
        self.bbox = BBox(bbox=list(self.vectors.geometry.total_bounds),
                         crs=self.vectors.crs['init'])
        self.possible_labels = list(self.vectors.LAND_TYPE.unique())
        self.ndvi_img = get_ndvi(self.bbox, query_date, eval_script)

    def get_statistics(self, query):
        try:
            if isinstance(query, int):
                polygon = [self.vectors.loc[query].geometry]
            elif all([isinstance(query, str), query in self.possible_labels]):
                land_type = self.vectors.loc[self.vectors['LAND_TYPE'] == query]
                polygon = land_type.dissolve(by='LAND_TYPE').geometry.values[0]
            
            query_mask = rasterio.features.rasterize(
                polygon, self.ndvi_img.raster.shape, -27365, 
                transform=self.ndvi_img.transform, all_touched=False)
            ndvi_masked = np.copy(self.ndvi_img.raster)
            ndvi_masked[query_mask == -27365] = np.nan
            
            return (round(np.nanmin(ndvi_masked), 6), 
                   round(np.nanmax(ndvi_masked), 6), 
                   round(np.nanmean(ndvi_masked), 6), 
                   round(np.nanstd(ndvi_masked), 6))
        except Exception as e:
            print(e)
            print('Query does not match with any ID nor LAND_TYPE')
            exit(0)


    def get_closest_pair(self, id_list, *criteria):
        mins_dict = {}
        abs_min = 10**20
        the_pair = ''
        t0 = datetime.datetime.now()
        #geos = list(self.vectors.loc[id_list].geometry.values)
        stats_by_item =list(map(self.get_statistics, id_list))
        stats_by_item = [dict(zip(
            ['min', 'max', 'mean', 'std'],i)) for i in stats_by_item]
        print(datetime.datetime.now() - t0)
        for i1,v1 in enumerate(stats_by_item):
            for i2,v2 in enumerate(stats_by_item):
                if i1 != i2:
                    if len(criteria) > 1:
                        diff = np.sqrt(
                            (v1[criteria[0]]-v2[criteria[0]])**2 + (
                                v1[criteria[1]]-v2[criteria[1]])**2)
                    else:
                        diff = abs(v1[criteria[0]]-v2[criteria[0]])
                    if diff < abs_min:
                        abs_min = diff
                        the_pair = (id_list[i1], id_list[i2])
        return the_pair


# class DeveloperEntryTask():

#     def __init__(self):
#         t0 = datetime.datetime.now()
#         query_date = query_date = '2018-09-28'
#         eval_script = 'return [B04,B08]'
#         shp_path = os.path.join(os.getcwd(), 'resources/polygons/land_polygons.shp')
#         vectors = geopandas.read_file(shp_path)
#         bbox = BBox(bbox=list(vectors.geometry.total_bounds),
#                 crs=vectors.crs['init'])
        
#         self.possible_labels = list(vectors.LAND_TYPE.unique())
#         vectors_list = vectors.geometry.values
#         land_type_polygons = vectors.groupby('LAND_TYPE')
#         land_type_polygons = []
        
#         # {
#         #     lt : vectors.loc[vectors['LAND_TYPE'] == lt
#         #     ].dissolve(by='LAND_TYPE').geometry.values[0]
#         #      for lt in self.possible_labels}
#         # # for i in range(len(vectors_list)):
#         #     land_type_polygons.update({i : vectors_list[i]})

#         self.ndvi_img = get_ndvi(bbox, query_date, eval_script)
#         land_type_dict = {}
#         for key, value in land_type_polygons.items():
#             land_type_dict[key] = get_polygon_stats(value, self.ndvi_img)
#         rasters_list = list(
#             map(
#                 functools.partial(
#                     get_polygon_stats, img=self.ndvi_img), 
#                     vectors_list))
#         print(datetime.datetime.now() - t0)
#         print(123)
#         self.rasters_dict = rasters_dict


    # def get_statistics(self, query):
    #     try:
    #         np_raster = self.rasters_dict[query]/Config.RESAMPLE_VAL
    #         return round(np)
    #         stats = get_polygon_stats(polygon, ndvi_img)
    #         stats = [round(i/Config.RESAMPLE_VAL,6) for i in stats]
    #         print(stats)
    #         return stats
    #     except:
    #         print('Query does not match with any ID nor LAND_TYPE')
    #         exit(0)


    # def get_closest_pair(id_list, *criteria):
    #     t0 = datetime.datetime.now()

    #     query_date = query_date = '2018-09-28'
    #     eval_script = 'return [B04,B08]'
    #     shp_path = os.path.join(os.getcwd(), 'resources/polygons/land_polygons.shp')

    #     vectors = geopandas.read_file(shp_path)
    #     bbox = BBox(bbox=list(vectors.geometry.total_bounds),
    #                 crs=vectors.crs['init'])

    #     ndvi_img = get_ndvi(bbox, query_date, eval_script)

        
    #     vectors['min']=None
    #     vectors['max']=None
    #     vectors['mean']=None
    #     vectors['std']=None
    #     index_stats = {}
