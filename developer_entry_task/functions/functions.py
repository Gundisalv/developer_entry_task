import os

import geopandas
import numpy as np
import rasterio.features
from sentinelhub import BBox
from shapely.geometry import mapping

from config import Config
from developer_entry_task.functions.maths import (min_dist_line,
                                                      min_dist_plane)
from developer_entry_task.functions.rasters import get_ndvi
from log import get_logger

logger = get_logger(__name__)


class DeveloperEntryTask():
    '''
    Class created for this thask. The constructor loads the images and poligons
    of the task. It also generates a numpy array containing the valid piexls
    where the polygons are.

    The class has two main fuctions: get_statistics and get_closest_pair.
    
    The first one returns a tuple of min, max, mean and std values for the 
    polygon ID or class string used in the query.

    The second one returns the polygon ID of a pair of polygons that are closest 
    to each other according with the statistical criteria or criterias given in 
    the arguments.
    '''

    def __init__(self):
        query_date = '2018-09-28'
        eval_script = 'return [B04,B08]'
        shp_path = os.path.join(
            os.getcwd(), 'resources/polygons/land_polygons.shp')
        self.vectors = geopandas.read_file(shp_path)
        self.bbox = BBox(bbox=list(self.vectors.geometry.total_bounds),
                         crs=self.vectors.crs['init'])
        self.possible_labels = list(self.vectors.LAND_TYPE.unique())
        self.class_value = dict(
            zip(self.possible_labels, range(len(self.possible_labels))))
        self.ndvi_img = get_ndvi(self.bbox, query_date, eval_script)
        self._rasterize_vectors()

    def _rasterize_vectors(self):
        '''
        Function to transform al vectors in the GeopandasDataFrame to a numpy
        array. All polygons are merged in one array where each polygon valid
        pixels have the polygon ID assigned as value (self.id_rasts).

        It also creates another raster similar to self.id_rasts, but of in this
        case all polygons of same class have theyr pixels assigned with the 
        same value.
        '''
        polygons_val = [
            (r['geometry'], int(i), int(self.class_value[r['LAND_TYPE']]))
            for i, r in self.vectors.iterrows()]
        id_rasts = np.zeros(self.ndvi_img.raster.shape) * np.nan
        class_rasts = np.zeros(self.ndvi_img.raster.shape) * np.nan
        self.id_rasts = rasterio.features.rasterize(
            ((mapping(p), v1) for p, v1, v2 in polygons_val),
            self.ndvi_img.raster.shape,  transform=self.ndvi_img.transform,
            all_touched=False, out=id_rasts)
        self.class_rasts = rasterio.features.rasterize(
            ((mapping(p), v2) for p, v1, v2 in polygons_val),
            self.ndvi_img.raster.shape,  transform=self.ndvi_img.transform,
            all_touched=False, out=class_rasts)

    def get_statistics(self, query):
        '''
        Returns a tuple of min, max, mean and std values for the polygon ID or 
        class string used in the query.

        query (str or int): This could be a string with a class name or an int
        corresponding to a polygon ID i.e.: 'grassland', 'forest', 1, 3, 9999.
        '''
        try:
            if all([isinstance(query, str), query in self.possible_labels]):
                query = self.class_value[query]
                return (
                    round(
                        np.nanmin(
                            self.ndvi_img.raster[
                                self.class_rasts == query]), 6),
                    round(
                        np.nanmax(
                            self.ndvi_img.raster[
                                self.class_rasts == query]), 6),
                    round(
                        np.nanmean(
                            self.ndvi_img.raster[
                                self.class_rasts == query]), 6),
                    round(
                        np.nanstd(
                            self.ndvi_img.raster[
                                self.class_rasts == query]), 6)
                    )
            elif all([isinstance(query, int), query < len(self.vectors)]):
                return (
                    round(
                        np.nanmin(
                            self.ndvi_img.raster[self.id_rasts == query]), 6),
                    round(
                        np.nanmax(
                            self.ndvi_img.raster[self.id_rasts == query]), 6),
                    round(
                        np.nanmean(
                            self.ndvi_img.raster[self.id_rasts == query]), 6),
                    round(
                        np.nanstd(
                            self.ndvi_img.raster[self.id_rasts == query]), 6))
        except:
            print('Query does not match with any ID nor LAND_TYPE')
            exit(0)

    def get_closest_pair(self, id_list, *criteria):
        '''
        Returns the polygon ID of a pair of polygons that are closest to each
        other according with the statistical criteria or criterias given in the
        arguments.

        id_list (list(int)): It is a list of three or more polygon IDs.
        *criteria (list(str)): A list of one or two statistical parameters of 
        this list 'min', 'max', 'mean', 'std'.
        '''
        try:
            stats_by_item = list(map(self.get_statistics, id_list))
            stats_by_item = [dict(zip(
                ['min', 'max', 'mean', 'std'], i)) for i in stats_by_item]
        except:
            print('Query does not match with any ID nor LAND_TYPE')
            exit(0)
        try:
            if len(criteria) == 1:
                points = [(v[criteria[0]], i)
                          for i, v in enumerate(stats_by_item)]
                pair = min_dist_line(points)
                return (id_list[pair[0]], id_list[pair[1]])
            elif len(criteria) > 1:
                index_pairs = sorted([([v[criteria[0]], v[criteria[1]]], i)
                                      for i, v in enumerate(stats_by_item)])

                points_c1 = [v[0][0] for i, v in enumerate(index_pairs)]

                points_c2 = [v[0][1] for i, v in enumerate(index_pairs)]
                value_pair = min_dist_plane(points_c1, points_c2)
                pair = sorted([i for v, i in index_pairs if any(
                    [v == list(value_pair[0]), v == list(value_pair[1])])])
                return (pair[0], pair[1])
        except:
            print('Error getting closest pair')
            exit(0)
        