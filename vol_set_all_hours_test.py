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
    """Runs function in tmpdir"""
    p = str(tmpdir)
    emmebank = os.path.join(os.getcwd(), 'emmebank')
    shutil.copyfile(emmebank, os.path.join(p, 'emmebank'))
    vol_set.new_project(p)
    new_project_dir = os.path.join(p, 'New_Project')
    new_project_file = os.path.join(new_project_dir, 'New_Project.emp')
    assert os.path.isdir(new_project_dir) is True
    assert os.path.isfile(new_project_file) is True


def test_new_project_exists(tmpdir):
    """test for existing New_Project folder behavior."""
    p = str(tmpdir)
    tmpdir.mkdir('New_Project')
    emmebank = os.path.join(os.getcwd(), 'emmebank')
    shutil.copyfile(emmebank, os.path.join(p, 'emmebank'))
    vol_set.new_project(p)
    new_project_dir = os.path.join(p, 'New_Project')
    new_project_file = os.path.join(new_project_dir, 'New_Project.emp')
    assert os.path.isdir(new_project_dir) is True
    assert os.path.isfile(new_project_file) is True


def test_shapefile_export():
    pass


def test_attribute_copy():
    pass
