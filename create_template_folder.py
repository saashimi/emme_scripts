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
import shutil


def copy_template_folder(working_dir):
    """Copies TBM template files into current directory.
    args: working_dir - the current working directory.
    returns: None.
    """
    templ_copy_dir = 'V:/tbm/kate/inroProjectTemplate/Metro_Project'
    # Check for existing project folder.
    project_folders = ['Metro_Project', 'New_Project']
    for project in project_folders:
        if os.path.isdir(project):
            overwrite = raw_input(project + ' folder exists! Delete? (y/n)\n')
            if overwrite.lower() == 'y':
                shutil.rmtree(os.path.join(working_dir, project))
                continue
            if overwrite.lower() == 'n':
                print('Exiting program without creating new Metro_Project!.')
                break
            else:
                print('Invalid option! Exiting program!')
                break
    # Write project folder if none exists.
    if not os.path.isdir('Metro_Project'):
        shutil.copytree(templ_copy_dir,
                        os.path.join(working_dir, 'Metro_Project'))
        print('Copied new Metro_Project folder.')


def path_edits(working_dir):
    """Writes appropriate path corrections to files based on the current
    working directory.
    args: working_dir - current working directory.
    returns: None.
    """
    files = ['Metro_Project.emp',
             'Views/Initial.emv',
             'Views/RTP18_los.emv']

    # This is the path currently found in the template files.
    old_path = '<WORKING_DIRECTORY>'
    project_path = os.path.join(working_dir, 'Metro_Project')

    for file in files:
        with open(os.path.join(project_path, file), 'r') as src:
            filedata = src.read()
        current_dir_str = working_dir.replace('\\', '/') + '/'
        filedata = filedata.replace(old_path, current_dir_str)
        with open(os.path.join(project_path, file), 'w') as src:
            src.write(filedata)


def main():
    """Main program control flow."""
    project_path = os.getcwd()
    copy_template_folder(project_path)
    path_edits(project_path)


if __name__ == '__main__':
    main()
