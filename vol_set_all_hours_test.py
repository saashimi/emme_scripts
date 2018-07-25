"""
Run this test file from a cygwin window on a server that contains the INRO
python API.
"""

import vol_set_all_hours as vol_set
from vol_set_all_hours import os, shutil


def test_new_project_does_not_exist(tmpdir):
    """Runs function in tmpdir"""
    emmebank = os.path.join(os.getcwd(), 'emmebank')
    shutil.copyfile(emmebank, os.path.join(str(tmpdir), 'emmebank'))
    vol_set.new_project(str(tmpdir))
    assert os.path.exists('tmpdir') is True
    assert os.path.isfile('New_Project') is True


def new_project_exists():
    """test for existing project behavior."""
    pass
