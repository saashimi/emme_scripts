"""
Run this script from the directory containing your emmebank
e.g. ../model/peak/assignPeakSpread/
"""

import inro.emme.database.emmebank as _emmebank


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

      
if __name__ == '__main__':
    main()
