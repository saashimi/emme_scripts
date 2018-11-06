"""
Test file for create_template_folder.py
"""

import create_template_folder as ctf
from create_template_folder import os
import __builtin__
import mock


def test_no_existing_folders(tmpdir):
    """
    Test case for no existing `Metro_Project` or `New_Folder` folders.
    Should not prompt for user interaction.
    """
    p = str(tmpdir)
    ctf.copy_template_folder(p)  # Creates a `Metro_Project` Folder
    project_folder = os.path.join(p, 'Metro_Project')
    assert os.path.isdir(project_folder) is True
    assert len(os.listdir(project_folder)) == 10


def test_Metro_Project_folder_exists(tmpdir):
    p = str(tmpdir)
    tmpdir.mkdir('Metro_Project')
    with mock.patch.object(__builtin__, 'raw_input', lambda x: 'y'):
        ctf.copy_template_folder(p)
        project_folder = os.path.join(p, 'Metro_Project')
        assert os.path.isdir(project_folder) is True
        assert len(os.listdir(project_folder)) == 10


def test_New_Project_folder_exists(tmpdir):
    p = str(tmpdir)
    tmpdir.mkdir('New_Project')
    with mock.patch.object(__builtin__, 'raw_input', lambda x: 'y'):
        ctf.copy_template_folder(p)
        project_folder = os.path.join(p, 'Metro_Project')
        assert os.path.isdir(project_folder) is True
        assert len(os.listdir(project_folder)) == 10


def test_two_folders_exist(tmpdir):
    p = str(tmpdir)
    tmpdir.mkdir('Metro_Project')
    tmpdir.mkdir('New_Project')
    with mock.patch.object(__builtin__, 'raw_input', lambda x: 'y'):
        ctf.copy_template_folder(p)
        project_folder = os.path.join(p, 'Metro_Project')
        assert os.path.isdir(project_folder) is True
        assert len(os.listdir(project_folder)) == 10


def test_rewrite_path(tmpdir):
    p = str(tmpdir)
    ctf.copy_template_folder(p)  # Creates a `Metro_Project` Folder
    ctf.path_edits(p)
    project_folder = os.path.join(p, 'Metro_Project')
    emp_file = os.path.join(project_folder, 'Metro_Project.emp')
    emp_string = p + '\\' + 'emmebank;;windows-1252'
    emp_string = emp_string.replace('\\', '/')
    assert 'WORKING_DIRECTORY' not in open(emp_file).read()
    assert emp_string in open(emp_file).read()
