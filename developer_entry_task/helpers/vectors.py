

class GeoData:
    def __init__(self, geojson):
        self.polygon = shapely.geometry.shape(geojson)
        self.plot_bbox = BBox(bbox=self.polygon.bounds, crs=CRS.WGS84)

    def RasterGeoData(self, np_array):
        self.array_shape = np_array.shape
        self.transform = rasterio.transform.from_bounds(
            *self.plot_bbox.get_lower_left(),
            *self.plot_bbox.get_upper_right(),
            width=self.array_shape[1],
            height=self.array_shape[0])