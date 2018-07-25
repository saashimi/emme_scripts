"""
Creates Metro_Project Template folder
by Kevin Saavedra

Run this script from the directory where you would like the .emp file to
reside.
e.g. ../model/peak/assignPeakSpread/

Useage:
>>> python create_template_folder.py
"""

import os
import sys
import shutil


def copy_template_folder(working_dir):
    """Copies TBM template files into current directory"""
    templ_copy_dir = 'V:/tbm/kate/inroProjectTemplate/Metro_Project'
    try:
        shutil.rmtree(os.path.join(working_dir, 'Metro_Project'))
        shutil.copytree(templ_copy_dir, working_dir)

    except WindowsError:
        if os.path.exists(working_dir):
            shutil.copytree(templ_copy_dir,
                            os.path.join(working_dir, 'Metro_Project'))
        else:
            print 'Path does not exist. Please enter an existing path.'
            sys.exit()


def path_edits(working_dir):
    """Writes appropriate path corrections to files based on the current
       working directory."""
    files = ['Metro_Project.emp',
             'Views/Initial.emv',
             'Views/RTP18_los.emv']

    # This is the path currently found in the template files.
    old_path = 'H:/rtp/2018rtp/_round2/modelRuns/2015/iter4/model/peak/' \
               'assignPeakSpread/'

    project_path = os.path.join(working_dir, 'Metro_Project')

    for file in files:
        with open(os.path.join(project_path, file), 'r') as src:
            filedata = src.read()

        current_dir_str = working_dir.replace('\\', '/') + '/'
        bank_error_str = 'assignPeakSpreademmebank'
        bank_error_fix = 'assignPeakSpread\emmebank'
        filedata = filedata.replace(old_path, current_dir_str)
        filedata = filedata.replace(bank_error_str, bank_error_fix)

        with open(os.path.join(project_path, file), 'w') as src:
            src.write(filedata)


def main():
    """Main program control flow."""
    project_path = os.getcwd()
    path_edits(project_path)


if __name__ == '__main__':
    main()
