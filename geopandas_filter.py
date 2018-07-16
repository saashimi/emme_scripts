"""
tests with geopandas
"""

import geopandas as gpd
import os

def rename_fields(df_rename):
    df_rename = df_rename.rename(columns=
    {
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
    Should mirror ArcGIS SQL query:
    SELECT * WHERE
        MODES LIKE '%c%'
        AND (VDF IN (1, 2, 4, 9, 10))
        AND NOT TYPE = 40
    """
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
    Filters for intersecting points only.
    """
    df_join = gpd.sjoin(df_shp, df_shp_intersects, op='intersects')
    return df_join


def main():
    working_dir = os.path.join(
        os.getcwd(), "New_Project/Media/Python_exported_scenario/")
    df_links = gpd.read_file(os.path.join(working_dir, "emme_links.shp"))
    df_nodes = gpd.read_file(os.path.join(working_dir, "emme_nodes.shp"))
    
    df_links = rename_fields(df_links)
    df_links = links_filter(df_links)
    df_links.to_file('output_links.shp', driver='ESRI Shapefile')
        
    df_nodes = intersect_filter(df_nodes, df_links)
    df_nodes.to_file('output_nodes.shp', driver='ESRI Shapefile')


if __name__ == '__main__':
    main()
