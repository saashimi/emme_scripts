"""
vol_set_all_hours.py
by Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov
Run this script from the directory containing your emmebank
e.g. ../model/peak/assignPeakSpread/
Useage:
>> python vol_set_all_hours.py
"""

import os
import sys
import shutil
import inro.emme.database.emmebank as _emmebank
import inro.emme.desktop.app as _app
import inro.modeller as _m


def new_project(working_dir):
    """Filter
    """
    emmebank_path = os.path.join(working_dir, "emmebank")
    try:    
        shutil.rmtree(os.path.join(working_dir,"New_Project"))
        project = _app.create_project(working_dir,"New_Project")
    except WindowsError:
        if os.path.exists(working_dir):
            project = _app.create_project(working_dir,"New_Project")
        else:
            print "Path does not exist. Please enter an existing path."
            sys.exit()        
    
    my_app = _app.start_dedicated(False, "000", project)
    data = my_app.data_explorer()
    bank = data.add_database(emmebank_path)
    return my_app, bank


def shapefile_export(working_dir, scenario, app):
    """Exports emme network as ArcGIS shapefile using standard modeller 
    toolbox."""
    print 'Exporting shapefile...'
    export_path = os.path.join(working_dir, 
                               "New_Project/Media/Python_exported_scenario")
    my_modeller = _m.Modeller(app)
    network_2_shp = my_modeller.tool(
        "inro.emme.data.network.export_network_as_shapefile"
    )
    selection = {
        "node": "all", 
        "link": "all", 
        "turn": "all",
        "transit_line": "all"
    }
    network_2_shp(export_path, False, 'SEGMENTS', scenario, selection)
    print 'Completed exporting shapefile.'


def attribute_copy(bank_in):
    print 'Copying attributes...'
    updates = {'@am0708': 2007, '@am0809': 2008}

    for key in updates:
        if key not in bank_in.scenario(2017).attributes('LINK'):
            bank_in.scenario(2017).create_extra_attribute('LINK', key)
            temp = bank_in.scenario(updates[key]).get_attribute_values('LINK', ['auto_volume'])
            bank_in.scenario(2017).set_attribute_values('LINK', [key], temp)
=
    temp_ul1 = bank_in.scenario(2012).get_attribute_values('LINK', ['auto_volume'])
    bank_in.scenario(2017).set_attribute_values('LINK', ['data1'], temp_ul1)
    temp_ul2 = bank_in.scenario(2016).get_attribute_values('LINK', ['auto_volume'])
    bank_in.scenario(2017).set_attribute_values('LINK', ['data2'], temp_ul2)
    print 'Completed copying attributes.'
    

def main():
    project_path = os.getcwd()
    new_app, new_bank = new_project(project_path)
    new_bank.open()
    attribute_copy(new_bank.core_emmebank)
    shapefile_export(project_path, new_bank.core_emmebank.scenario(2017), new_app)
    new_bank.close()


if __name__ == '__main__':
    main()
