"""
Run this script from the directory containing your emmebank
e.g. ../model/peak/assignPeakSpread/
Useage:
>> python vol_set_all_hours.py
"""

import os
import inro.emme.database.emmebank as _emmebank
import inro.emme.desktop.app as _app
import inro.modeller as _m

def shapefile_export(scenario):
    """Exports emme network as ArcGIS shapefile using standard modeller 
    toolbox."""
    project_path = os.path.join(os.getcwd(), "New_Project/New_Project.emp")
    export_path = os.path.join(os.getcwd(),  "New_Project/Media/Python_exported_scenario")
    my_desktop = _app.start_dedicated(project = project_path, 
                                      visible  = False, 
                                      user_initials = "user")
    my_modeller = _m.Modeller(my_desktop)
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

def main():
    # TODO: try to refactor using a dictionary for inputs. 

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

    shapefile_export(_emmebank.Emmebank().scenario(2017))

      
if __name__ == '__main__':
    main()
