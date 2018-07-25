"""
Creates Metro_Project Template folder
"""

import os
import sys
import shutil
import inro.emme.desktop.app as _app


def new_project(working_dir):
    """Replaces `New_Project` directory and creates new .emp file."""
    emmebank_path = os.path.join(working_dir, 'emmebank')
    try:
        shutil.rmtree(os.path.join(working_dir, 'Metro_Project'))
        project = _app.create_project(working_dir, 'Metro_Project')
    except WindowsError:
        if os.path.exists(working_dir):
            project = _app.create_project(working_dir, 'Metro_Project')
        else:
            print 'Path does not exist. Please enter an existing path.'
            sys.exit()

    my_app = _app.start_dedicated(False, '000', project)
    data = my_app.data_explorer()
    bank = data.add_database(emmebank_path)
    return my_app, bank


def copy_template_files(working_dir):
    



def main():
    project_path = os.getcwd()
    new_app, new_bank = new_project(project_path)


if __name__ == '__main__':
    main()
