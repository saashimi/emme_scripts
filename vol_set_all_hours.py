"""
vol_set_all_hours.py
by Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov

Aggregates auto volume (volau) information into @am0708, @am0809, volau, ul1
and ul2 attributes into 2017 Scenario number for shapefile export and future
parsing.

Run this script from the directory containing your emmebank
e.g. ../model/peak/assignPeakSpread/
Useage:
>> python vol_set_all_hours.py

Note: If you have ArcCatalog or ArcGIS open on the output links.shp,
it will produce a lock on the shapefile that will prevent you from re-running
the script:
    `Cannot create a file when that file already exists.`
Make sure you do not have the links.shp selected at all if you need to run this
more than once.
"""

import os
import sys
import shutil
import inro.emme.desktop.app as _app
import inro.modeller as _m


def new_project(working_dir):
    """Replaces `New_Project` directory and creates new .emp file."""
    emmebank_path = os.path.join(working_dir, 'emmebank')
    try:
        shutil.rmtree(os.path.join(working_dir, 'New_Project'))
        project = _app.create_project(working_dir, 'New_Project')
    except WindowsError:
        if os.path.exists(working_dir):
            project = _app.create_project(working_dir, 'New_Project')
        else:
            print 'Path does not exist. Please enter an existing path.'
            sys.exit()

    my_app = _app.start_dedicated(False, '000', project)
    data = my_app.data_explorer()
    bank = data.add_database(emmebank_path)
    return my_app, bank


def shapefile_export(working_dir, scenario, app):
    """Exports emme network as ArcGIS shapefile using standard modeller
    toolbox."""
    print 'Exporting shapefile...'
    export_path = os.path.join(working_dir, 
                               'New_Project/Media/Python_exported_scenario')
    my_modeller = _m.Modeller(app)
    network_2_shp = my_modeller.tool(
        'inro.emme.data.network.export_network_as_shapefile'
    )
    selection = {
        'node': 'all',
        'link': 'all',
        'turn': 'all',
        'transit_line': 'all'
    }
    network_2_shp(export_path, False, 'SEGMENTS', scenario, selection)
    print 'Completed exporting shapefile.'


def attribute_copy(bank_in):
    """Aggregates volau attribute from the following times into 2017 scenario:
        @am0708: 0700-0800 from Scenario 2012
        @am0809: 0800-0900 from Scenario 2008
        ul1:     1200-1300 from Scenario 2012
        ul2:     1600-1700 from Scenario 2016
        volau:   1700-1800 from Scenario 2017 (current scenario)
    """
    print 'Copying attributes...'
    updates = {'@am0708': 2007, '@am0809': 2008}
    for key in updates:
        if key not in bank_in.scenario(2017).attributes('LINK'):
            bank_in.scenario(2017).create_extra_attribute(
                'LINK', key)
            temp = bank_in.scenario(updates[key]).get_attribute_values(
                'LINK', ['auto_volume'])
            bank_in.scenario(2017).set_attribute_values(
                'LINK', [key], temp)

    temp_ul1 = bank_in.scenario(2012).get_attribute_values(
        'LINK', ['auto_volume'])
    bank_in.scenario(2017).set_attribute_values(
        'LINK', ['data1'], temp_ul1)
    temp_ul2 = bank_in.scenario(2016).get_attribute_values(
        'LINK', ['auto_volume'])
    bank_in.scenario(2017).set_attribute_values(
        'LINK', ['data2'], temp_ul2)
    print 'Completed copying attributes.'


def main():
    project_path = os.getcwd()
    new_app, new_bank = new_project(project_path)
    new_bank.open()
    attribute_copy(new_bank.core_emmebank)
    shapefile_export(project_path, new_bank.core_emmebank.scenario(2017),
                     new_app)
    new_bank.close()


if __name__ == '__main__':
    main()
