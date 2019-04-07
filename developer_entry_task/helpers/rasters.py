from config import Config
from sentinelhub import WcsRequest, constants, DownloadFailedException
import numpy as np
import rasterio
from log import get_logger

logger = get_logger(__name__)


class GetSentinelHubImages(WcsRequest):

    def __init__(self, bbox, geometry=False, end_date='latest', start_date=None,
                 layer='NDVI', maxcc=0.30, to_nan=True, last=False,
                 save_data=False, eval_script=False, res='10m'):
        self.bbox = bbox
        self.save_data = save_data
        self.last = last
        self.to_nan = to_nan
        custom_url_params = {
            constants.CustomUrlParam.TRANSPARENT: True
        }
        if geometry:
            custom_url_params[constants.CustomUrlParam.GEOMETRY] = geometry
        if eval_script:
            custom_url_params[constants.CustomUrlParam.EVALSCRIPT] = eval_script
        if start_date is not None:
            time_tuple = (start_date, end_date)
        else:
            time_tuple = end_date

        try:
            WcsRequest.__init__(self, data_folder='./shub_downloads', layer=layer, 
                                bbox=bbox,
                                custom_url_params=custom_url_params,
                                maxcc=maxcc, time=time_tuple,
                                resx=res, resy=res,
                                image_format=constants.MimeType.TIFF_d32f,
                                instance_id=Config.SENTINEL_INSTANCE_ID)
        except DownloadFailedException:
            logger.error('Unable to stablish connection. '
                         'Please check your internet connection and try again.')
        self._run()

    def _run(self):
        try:
            self.metadata_list = list(self.get_tiles())
            self.dates_list = list(self.get_dates())
            if self.last:
                list_with_alpha = self.get_data(save_data=self.save_data,
                                                data_filter=[-1])
                self.metadata_list = self.metadata_list[-1]
                self.dates_list = self.dates_list[-1]
            else:
                list_with_alpha = self.get_data(save_data=self.save_data)
            if self.to_nan:
                self.images = list(map(nan_to_no_data, list_with_alpha))
            else:
                self.images = list_with_alpha
            if len(self.images) < 1:
                raise
        except:
            logger.error('No images found. Terminating.')
            exit(0)


class SentinelHubImage():

    def __init__(self, np_raster, bbox, date=None):
        self.raster = np_raster
        self.date = date
        self.transform = rasterio.transform.from_bounds(
            *bbox.get_lower_left(), *bbox.get_upper_right(),
            width=np_raster.shape[1], height=np_raster.shape[0])
        self.crs = {'init': bbox.crs.ogc_string()}

    def save_raster(self, file_name):
        with rasterio.open(file_name, 'w', driver='GTiff',
                           width=self.raster.shape[1],
                           height=self.raster.shape[0], count=1,
                           dtype=np.float64, nodata=np.nan,
                           transform=self.transform,
                           crs=self.crs) as dst:
            dst.write(self.raster.astype(np.float64), indexes=1)

    def _run_stats(self):
        self.min = round(np.nanmin(self.raster),6)
        self.max = round(np.nanmax(self.raster),6)
        self.mean = round(np.nanmean(self.raster),6)
        self.median = round(np.nanmedian(self.raster),6)
        self.std = round(np.nanstd(self.raster),6)
        self.range = round(self.max - self.min,6)


def nan_to_no_data(img):
    img[:, :, 0][img[:, :, 1] == 0] = np.nan
    return img[:, :, 0]
