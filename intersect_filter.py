"""
Spatial filter test
"""

from osgeo import ogr, gdal
import os


def intersect_filter(dir, shp_in, shp_filter_against):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.Open(shp_in, 0)
    data_layer = data_source.GetLayer(0)
    filter_source = driver.Open(shp_filter_against, 0)
    
    data_layer.SetSpatialFilter(filter_source)
    
    #return data_layer, data_source
    out_shapefile = os.path.join(dir, 'out_shapefile.shp')
    out_ds = driver.CreateDataSource(out_shapefile)
    out_layer = out_ds.CopyLayer(data_layer, 'intersections_only')
    del data_layer, data_source, out_ds, out_layer

def main():
    working_dir = os.path.join(
        os.getcwd(), "New_Project/Media/Python_exported_scenario/")
    shp = os.path.join(working_dir, "emme_links.shp")
    nodes = os.path.join(working_dir, "emme_nodes.shp")
    intersect_filter(working_dir, nodes, shp)


if __name__ == '__main__':
    main()
