# emme_scripts

These are scripts developed for Metro's Travel Demand Model. 

### Prerequisites

* Python 2.7
* INRO Emme

### Files and descriptions

* create_template_folder.py - Copies Metro_Project folder from template folder location and changes path information to current working directory.
* vol_set_all_hours.py - Aggregates auto volume (volau) information into @am0708, @am0809, volau, ul1, and ul2 attributes into 2017 Scenario number for shapefile export and future parsing.
* emme_shp_final_output.py - Performs cleanup on output shapefiles resulting from vol_set_hours.py. Selects only nodes and links of interest and sets projection to OR Stateplane N.


## Authors

Kevin Saavedra