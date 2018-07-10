"""
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
    emmebank_path = os.path.join(working_dir, "emmebank")
    try:    
        shutil.rmtree(os.path.join(working_dir,"New_Project"))
        project = _app.create_project(working_dir,"New_Project")#change to relative path
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
    #emp_project_path = os.path.join(working_dir, "New_Project/New_Project.emp")
    export_path = os.path.join(working_dir,  "New_Project/Media/Python_exported_scenario")
    #my_desktop = _app.start_dedicated(project = emp_project_path, 
    #                                  visible  = False, 
    #                                  user_initials = "user")
    #my_modeller = _m.Modeller(my_desktop)
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

def attribute_copy():
    if '@am0708' not in _emmebank.Emmebank().scenario(2017).attributes('LINK'):
        _emmebank.Emmebank().scenario(2017).create_extra_attribute('LINK', '@am0708')
        temp_0708 = _emmebank.Emmebank().scenario(2007).get_attribute_values('LINK', ['auto_volume'])
        _emmebank.Emmebank().scenario(2017).set_attribute_values('LINK', ['@am0708'], temp_0708)

    if '@am0809' not in _emmebank.Emmebank().scenario(2017).attributes('LINK'):
        _emmebank.Emmebank().scenario(2017).create_extra_attribute('LINK', '@am0809')
        temp_0809 = _emmebank.Emmebank().scenario(2008).get_attribute_values('LINK', ['auto_volume'])
        _emmebank.Emmebank().scenario(2017).set_attribute_values('LINK', ['@am0809'], temp_0809)

    temp_ul1 = _emmebank.Emmebank().scenario(2012).get_attribute_values('LINK', ['auto_volume'])
    _emmebank.Emmebank().scenario(2017).set_attribute_values('LINK', ['data1'], temp_ul1)
    temp_ul2 = _emmebank.Emmebank().scenario(2016).get_attribute_values('LINK', ['auto_volume'])
    _emmebank.Emmebank().scenario(2017).set_attribute_values('LINK', ['data2'], temp_ul2)
    

def main():
    project_path = os.getcwd()
    new_app, new_bank = new_project(project_path)
    new_bank.open()
    shapefile_export(project_path, new_bank.core_emmebank.scenario(2017), new_app)
    new_bank.close()
    # TODO: try to refactor using a dictionary for inputs. 
      
if __name__ == '__main__':
    main()
