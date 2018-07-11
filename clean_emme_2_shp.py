"""
Preliminary script
clean_emme_2_shp.py
"""

from osgeo import ogr, gdal
import os


def rename_fields(shp_in):
    data_source = gdal.OpenEx(shp_in, gdal.OF_VECTOR | gdal.OF_UPDATE)

    rename = {'@am0708': 'VOLS_07_08',
              '@am0809': 'VOLS_08_09',
              'DATA1': 'VOLS_12_13',
              'DATA2': 'VOLS_16_17',
              'VOLAU': 'VOLS_17_18',
              'DATA3': 'APP_CAP',
              '@mb': 'MB_CAP'}

    for key in rename:
        data_source.ExecuteSQL('ALTER TABLE {} RENAME COLUMN {} TO {}'
                               .format('emme_links', key, rename[key]))


def filter_shp(dir, shp_in):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.Open(shp_in, 0)

    sql = """SELECT ID, INODE, JNODE, LENGTH, MODES, LANES, VDF, TYPE,
          VOLS_07_08, VOLS_08_09, VOLS_12_13, VOLS_16_17, VOLS_17_18,
          MB_CAP FROM {} WHERE
          MODES LIKE '%c%'
          AND (VDF IN (1, 2, 4, 9, 10))
          AND NOT TYPE = 40
          """.format('emme_links')

    input_layer = data_source.ExecuteSQL(sql)
    out_shapefile = os.path.join(dir, 'out_shapefile.shp')
    out_ds = driver.CreateDataSource(out_shapefile)
    out_layer = out_ds.CopyLayer(input_layer, 'output_layer')
    del input_layer, data_source, out_ds, out_layer


def main():
    working_dir = os.path.join(
        os.getcwd(), "New_Project/Media/Python_exported_scenario/")
    shp = os.path.join(working_dir, "emme_links.shp")
    #rename_fields(shp)
    filter_shp(working_dir, shp)


if __name__ == '__main__':
    main()
