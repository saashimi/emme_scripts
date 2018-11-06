"""
Test file for 24_hr_d221_split.py
"""

import d221_24hr_split as d221
from d221_24hr_split import pd
import pytest


def test_load_xlsx():
    test_path = 'H:/rtp/2018rtp/_round2/modelRuns/2015/development/'\
                'Inputs_2015_Kate_DEV.xlsx'
    df = d221.load_xlsx(test_path, 'HW_0001')
    column_list = ['VEH_ID', 'VEH_NAME', 'VEH_MODE', 'VEH_CLASS',
                   'DEFAULT_SPEED', 'TRIMET_TYPE', 'DIRECTIONAL',
                   'TRIMET_NAME', 'HW_0001', 'HW_0102', 'HW_0203',
                   'HW_0304', 'HW_0405', 'HW_0506', 'HW_0607', 'HW_0708',
                   'HW_0809', 'HW_0910', 'HW_1011', 'HW_1112', 'HW_1213',
                   'HW_1314', 'HW_1415', 'HW_1516', 'HW_1617', 'HW_1718',
                   'HW_1819', 'HW_1920', 'HW_2021', 'HW_2122', 'HW_2223',
                   'HW_2324']
    assert sorted(df.columns) == sorted(column_list)


def test_filter_valid_transit():
    test_path = 'H:/rtp/2018rtp/_round2/modelRuns/2015/development/'\
                'Inputs_2015_Kate_DEV.xlsx'
    hour = 'HW_0001'
    df = d221.load_xlsx(test_path, hour)
    # TODO: CHECK BEST PRACTICES ON RELIANCE ON EARLIER TESTS
    filter_valid_transit_output = d221.filter_valid_transit(df, hour)
    transit_list_expected = ['01Ba', '01Bb', '01Ga', '01Gb',  '01Ra', '01Rb',
                             '01YOa', '01YOb', '12TPa', '12TPb', '33CCa',
                             '33CCb', '57F', '75Ca', '75Cb', 'C04a', 'C04b']
    assert sorted(filter_valid_transit_output) == sorted(transit_list_expected)


def test_clean_and_list():
    test_raw_header = "a'01Ba  ' l   1   7.00   6.00 'BLUE   HILLS/GRESHa '      7     15      0"
    clean_and_list_output = d221.clean_and_list(test_raw_header)
    expected_list = ['01Ba', 'l', '1', '7.00', '6.00', "'BLUE HILLS/GRESHa'",
                     '7', '15', '0']
    assert sorted(clean_and_list_output) == sorted(expected_list)


def test_header_parser():
    hour = 'HW_0001'
    test_header_list = ['01Ba', 'l', '1', '7.00', '6.00', "'BLUE HILLS/GRESHa'",
                        '7', '15', '0']
    d = {'VEH_ID': ['01Ba'], 'HW_0001': [30]}
    df_test = pd.DataFrame(data=d)

    header_parser_output = d221.header_parser(test_header_list, hour, df_test)
    expected_list = ["a'01Ba'", 'l', '1', '30', '6.00', "'BLUE HILLS/GRESHa'",
                     '0', '0', '0']

    assert sorted(header_parser_output) == sorted(expected_list)


@pytest.mark.skip(reason="easier to manually check output in emme via batchin.")
def test_main():
    pass
