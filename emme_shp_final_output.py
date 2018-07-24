"""
emme_shp_final_output.py
by Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov

Performs cleanup on output shapefiles resulting from vol_set_hours.py.

Run this script from the directory containing your emmebank
e.g. ../model/peak/assignPeakSpread/

Useage:
>>> python emme_shp_final_output.py

Requirements:
geopandas library.
"""

import geopandas as gpd
import os


def rename_fields(df_rename):
    """Renames default output from vol_set_hours.py script into standalone
    ArcGIS shapefile fields.
    Args: df_rename, a geopandas dataframe.
    Returns: df_rename, a geopandas dataframe with final renamed columns.
    """
    df_rename = df_rename.rename(columns={
        '@am0708': 'VOLS_07_08',
        '@am0809': 'VOLS_08_09',
        'DATA1': 'VOLS_12_13',
        'DATA2': 'VOLS_16_17',
        'VOLAU': 'VOLS_17_18',
        'DATA3': 'APP_CAP',
        '@mb': 'MB_CAP'
    })
    return df_rename


def links_filter(df_links_in):
    """
    Filters links that should mimic the ArcGIS SQL query:
    ---------------------------------
    SELECT * WHERE
        MODES LIKE '%c%'                  # AUTO MODES
        AND (VDF IN (1, 2, 4, 9, 10))     # 1 = FWY, 2 = APPROACH, 4 = MIDBLOCK
                                          # 9 = PORTLAND CBD, 10 = RAMP METERS
        AND NOT TYPE = 40                 # STUB LINKS
    ---------------------------------
    Args: df_links_in, a geopandas dataframe
    Returns: df_relevant, a geopandas dataframe with filtered links
    """
    print 'Filtering links...'
    df_relevant = df_links_in[
        (df_links_in['MODES'].str.contains('c')) &
        (df_links_in['VDF'].isin([1, 2, 4, 9, 10])) &
        (df_links_in['TYPE'] != 40)]

    usecols = ['ID', 'INODE', 'JNODE', 'LENGTH', 'MODES', 'LANES', 'VDF', 
               'TYPE', 'VOLS_07_08', 'VOLS_08_09', 'VOLS_12_13', 'VOLS_16_17',
               'VOLS_17_18', 'APP_CAP', 'MB_CAP', 'geometry']

    df_relevant = df_relevant[usecols]
    return df_relevant


def intersect_filter(df_shp, df_shp_intersects):
    """
    Filters for points that intersect a filtered roadway network.
    Args:
    df_shp, a geopandas dataframe containing nodes
    df_shp_intersects, a geopandas dataframe containing links.
    Returns:
    df_join, a geopandas dataframe with final intersecting nodes only, and
    with only relevant fields.
    """
    print "Determining node/link intersections..."
    df_join = gpd.sjoin(df_shp, df_shp_intersects, op='intersects')
    df_join = df_join[['ID_left', 'X', 'Y', 'geometry']]
    df_join = df_join.rename(columns={'ID_left': 'ID'})
    # TODO: INVESTIGATE WHY THERE ARE SO MANY DUPLICATE NODES FROM THIS STEP
    df_join = df_join.drop_duplicates(['ID', 'X', 'Y']) 
    return df_join


def main():
    """
    Main program flow.
    """
    working_dir = os.path.join(
        os.getcwd(), 'New_Project/Media/Python_exported_scenario/')
    print 'Loading files...'
    df_links = gpd.read_file(os.path.join(working_dir, "emme_links.shp"))
    df_links.crs = {'init': 'epsg:2913'}
    df_nodes = gpd.read_file(os.path.join(working_dir, "emme_nodes.shp"))
    df_nodes.crs = {'init': 'epsg:2913'}

    df_links = rename_fields(df_links)
    df_links = links_filter(df_links)
    print 'Exporting links...'
    df_links.to_file(
        'New_Project/Media/Python_exported_scenario/output_links.shp', 
        driver='ESRI Shapefile')

    df_nodes = intersect_filter(df_nodes, df_links)
    print 'Exporting nodes...'
    df_nodes.to_file(
        'New_Project/Media/Python_exported_scenario/output_nodes.shp',
        driver='ESRI Shapefile')
    print 'Script completed.'


if __name__ == '__main__':
    main()
