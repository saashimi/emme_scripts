"""
vol_set_all_hours_test.py
by Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov

Run this test file from a cygwin window on a server that contains the INRO
python API.

USEAGE:
>>> pytest vol_set_all_hours_test.py
"""

import vol_set_all_hours as vol_set
from vol_set_all_hours import os, shutil


def test_new_project_does_not_exist(tmpdir):
    # Runs function in tmpdir
    p = str(tmpdir)
    emmebank = os.path.join(os.getcwd(), 'emmebank')
    shutil.copyfile(emmebank, os.path.join(p, 'emmebank'))
    vol_set.Metro_Project(p)
    new_project_dir = os.path.join(p, 'Metro_Project')
    new_project_file = os.path.join(new_project_dir, 'Metro_Project.emp')
    assert os.path.isdir(new_project_dir) is True
    assert os.path.isfile(new_project_file) is True


def test_new_project_exists(tmpdir):
    # test for existing Metro_Project folder behavior
    p = str(tmpdir)
    tmpdir.mkdir('Metro_Project')
    emmebank = os.path.join(os.getcwd(), 'emmebank')
    shutil.copyfile(emmebank, os.path.join(p, 'emmebank'))
    vol_set.Metro_Project(p)
    new_project_dir = os.path.join(p, 'Metro_Project')
    new_project_file = os.path.join(new_project_dir, 'Metro_Project.emp')
    assert os.path.isdir(new_project_dir) is True
    assert os.path.isfile(new_project_file) is True


def test_attribute_copy(tmpdir):
    p = str(tmpdir)
    emmebank = os.path.join(os.getcwd(), 'emmebank')
    shutil.copyfile(emmebank, os.path.join(p, 'emmebank'))
    test_app, test_bank = vol_set.Metro_Project(p)
    test_bank.open()
    vol_set.attribute_copy(test_bank.core_emmebank)
    test_bank.close()
    scen2017 = test_bank.core_emmebank.scenario(2017)
    tbce = test_bank.core_emmebank

    assert scen2017.extra_attribute('@am0708') is not None
    assert scen2017.extra_attribute('@am0809') is not None
    assert scen2017.get_attribute_values('LINK', ['data1']) == (
        tbce.scenario(2012).get_attribute_values('LINK', ['auto_volume']))
    assert scen2017.get_attribute_values('LINK', ['data2']) == (
        tbce.scenario(2016).get_attribute_values('LINK', ['auto_volume']))

    """
    For whatever reason, the user-defined @am values have one more entry than
    the original copied scenario, and will raise assertion errors.
    THESE TESTS WILL ALWAYS FAIL EVEN THOUGH THEY ARE STRUCTURED SIMILARLY
    TO THE ABOVE ASSERTIONS:"""
    print len(scen2017.get_attribute_values('LINK', ['@am0708'])[1])
    print len(tbce.scenario(2007).get_attribute_values(
              'LINK', ['auto_volume'])[1])
    print len(scen2017.get_attribute_values('LINK', ['@am0809'])[1])
    print len(tbce.scenario(2008).get_attribute_values(
              'LINK', ['auto_volume'])[1])

    assert scen2017.get_attribute_values('LINK', ['@am0708']) == (
        tbce.scenario(2007).get_attribute_values('LINK', ['auto_volume']))
    assert scen2017.get_attribute_values('LINK', ['@am0809']) == (
        tbce.scenario(2008).get_attribute_values('LINK', ['auto_volume']))

    """THESE ARE THE WORKAROUND TESTS:"""
    workaround_0708 = scen2017.get_attribute_values('LINK',
                                                    ['@am0708'])[1][:-1]
    workaround_0809 = scen2017.get_attribute_values('LINK',
                                                    ['@am0809'])[1][:-1]
    assert workaround_0708 == (
        tbce.scenario(2007).get_attribute_values('LINK', ['auto_volume'])[1])
    assert workaround_0809 == (
        tbce.scenario(2008).get_attribute_values('LINK', ['auto_volume'])[1])

    assert sum(scen2017.get_attribute_values('LINK', ['@am0708'])[1]) == (
        sum(tbce.scenario(2007).get_attribute_values(
            'LINK', ['auto_volume'])[1]))
    assert sum(scen2017.get_attribute_values(
               'LINK', ['@am0809'])[1]) == (
        sum(tbce.scenario(2008).get_attribute_values(
            'LINK', ['auto_volume'])[1]))


def test_shapefile_export(tmpdir):
    # A more robust test could probably count the number of objects per
    # shapefile
    p = str(tmpdir)
    emmebank = os.path.join(os.getcwd(), 'emmebank')
    shutil.copyfile(emmebank, os.path.join(p, 'emmebank'))
    test_app, test_bank = vol_set.Metro_Project(p)
    test_bank.open()
    new_project_dir = os.path.join(p, 'Metro_Project')
    scenario = test_bank.core_emmebank.scenario(2017)
    vol_set.shapefile_export(p, scenario, test_app)
    export_path = os.path.join(new_project_dir, 'Media',
                               'Python_exported_scenario')
    assert os.path.isdir(export_path) is True
    assert len(os.listdir(export_path)) == 16
    test_bank.close()
