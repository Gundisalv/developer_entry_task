# In[]
from developer_entry_task.helpers.rasters import *
from developer_entry_task.helpers.vectors import *
from developer_entry_task.functions.functions import *
import geopandas
import os
from shapely.geometry import shape
from sentinelhub import BBox

# In[]

respath = os.path.join(os.getcwd(), 'resources/polygons/land_polygons.shp')
vectors = geopandas.read_file(respath)
bbox = BBox(bbox=list(vectors.geometry.total_bounds), crs=vectors.crs['init'])
query_date = '2018-09-28'
eval_script = 'return [B04,B08]'
response = GetSentinelHubImages(bbox=bbox, end_date=query_date, maxcc=1, 
                                eval_script=eval_script, save_data=True,
                                to_nan=False)

# In[]
ndvi_array = (response.images[0][:,:,1]-response.images[0][:,:,0])/(
              response.images[0][:,:,1]+response.images[0][:,:,0])

red_band = SentinelHubImage(response.images[0][:,:,0], bbox, response.dates_list[0])
nir_band = SentinelHubImage(response.images[0][:,:,1], bbox, response.dates_list[0])

ndvi_img = SentinelHubImage(ndvi_array, bbox, response.dates_list[0])

# In[]

ndvi_img.save_raster('kakska.tif')
# In[]

del response


print(123)

