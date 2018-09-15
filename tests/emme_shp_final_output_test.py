"""
Test file for emme_shp_final_output.py

by Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov
"""

import emme_shp_final_output as em_shp
from emme_shp_final_output import os
import pytest


def test_rename_fields():
    working_dir = os.path.join(
        os.getcwd(), 'Metro_Project', 'Media', 'Python_exported_scenario')
    test_df = em_shp.gpd.read_file(os.path.join(working_dir, "emme_links.shp"))
    test_df = em_shp.rename_fields(test_df)
    changed = ['@am0708', '@am0809', 'DATA1', 'DATA2', 'VOLAU', 'DATA3', '@mb']
    final = ['VOLS_07_08', 'VOLS_08_09', 'VOLS_12_13', 'VOLS_16_17',
             'VOLS_17_18', 'APP_CAP', 'MB_CAP']

    for item in changed:
        assert item not in list(test_df)
    for item in final:
        assert item in list(test_df)


def test_links_filter():
    working_dir = os.path.join(
        os.getcwd(), 'Metro_Project', 'Media', 'Python_exported_scenario')
    test_df = em_shp.gpd.read_file(os.path.join(working_dir, "emme_links.shp"))
    test_df = em_shp.gpd.read_file(os.path.join(
        working_dir, "emme_links.shp"))
    test_renamed_df = em_shp.rename_fields(test_df)
    test_filtered_df = em_shp.links_filter(test_renamed_df)
    cols = ['ID', 'INODE', 'JNODE', 'LENGTH', 'MODES', 'LANES', 'VDF',
            'TYPE', 'VOLS_07_08', 'VOLS_08_09', 'VOLS_12_13', 'VOLS_16_17',
            'VOLS_17_18', 'APP_CAP', 'MB_CAP', 'geometry']

    assert cols == list(test_filtered_df)
    vdf = [1, 2, 4, 9, 10]
    df_vdfs = em_shp.gpd.GeoSeries(list(test_filtered_df['VDF']))
    for item in df_vdfs:
        assert item in vdf

    df_modes = em_shp.gpd.GeoSeries(list(test_filtered_df['MODES']))
    for item in df_modes:
        for char in item:
            assert 'c' in item

    df_type = em_shp.gpd.GeoSeries(list(test_filtered_df['TYPE']))
    for item in df_type:
        assert 40 not in df_type


@pytest.mark.skip(reason="no way of currently testing this")
def test_intersect_filter():
    pass
