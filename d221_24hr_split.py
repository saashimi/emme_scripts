"""
d221_24_split.py

By: Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov

Reads d221 files and creates one unified d221 transit file per user indicated
hour.

Useage:
>>>> python d221_24hr_split.py <network_file> <excel_inputs_path>
                                <project_name> <emme_specified_hour>

e.x:
>> python d221_24hr_split.py d221.RTP18_2015_Base_pktr
                                     Inputs_2015_Kate_DEV.xlsx RTP18_2015 0001
"""


import sys
import os
import pandas as pd
import re


def load_xlsx(path_in, hour_in):
    """Loads excel input file.
    Input: path_in, the full path for the excel inputs file. 
           hour_in, an emme hour code as user arg.
    Returns: df_joined, a pandas dataframe
    """
    xlsx_file = os.path.abspath(path_in)
    df_transit_lines = pd.read_excel(xlsx_file, sheet_name='transit_lines')
    df_transit_types = pd.read_excel(xlsx_file, sheet_name='transit_types')
    df_joined = pd.merge(df_transit_lines, df_transit_types, on='TRIMET_TYPE')

    return df_joined


def filter_valid_transit(df_in, hour_in):
    """Filters master dataframe for VEH_IDs valid for specified hour
    Inputs: df_in, a pandas dataframe containing joined transit_lines and
            transit_types excel worksheets.
            hour_in, an emme hour code as user arg.
    Returns: transit_list, a list of valid VEH_IDs per specified hour
    """
    df_in = df_in[df_in[hour_in].notnull()]
    transit_list = df_in['VEH_ID'].tolist()

    return transit_list


def clean_and_list(header_in):
    """Converts raw text lines to cleaned lists.
    Input: header_in, the emme transit header line.
    Returns: header_list, a cleaned list of all transit header elements.
    """
    # regex everything between single quotes, e.g. 'BLUE    HILLS/GRESHa  '
    list_match = re.findall(r"'(.*?)'", header_in)

    # delete existing transit info
    header_in = header_in.replace(list_match[0], '')
    header_in = header_in.replace(list_match[1], '')
    header_list = list(filter(None, header_in.rstrip().split(' ')))

    # cleaned and stripped transit values
    # note that stripped_id does not yet contain a' formatting needed in emme!
    stripped_id = list_match[0].strip()
    stripped_name = "'" + ' '.join(list_match[1].split()) + "'"

    header_list[0] = stripped_id
    header_list[5] = stripped_name

    return header_list


def header_parser(list_in, hour_in, df_in):
    """Replaces existing headways based on excel lookup table values per given
    hour.
    Inputs: list_in, a cleaned list of all transit header elements.
            hour_in, an emme hour code as user arg.
            df_in, a pandas dataframe containing joined transit_lines and
            transit_types excel worksheets.
    Returns: list_in, input list but with edits for transit id, headway, and
             zeroed-out user_id fields.
    """
    transit_id = list_in[0]
    transit_lookup = df_in.loc[df_in['VEH_ID'] == transit_id]
    new_headway = str(transit_lookup[hour_in].tolist()[0])

    # Write new attributes
    formatted_transit_id = "a'" + transit_id + "'"
    list_in[0] = formatted_transit_id
    list_in[3] = new_headway

    # Zero out all the user attributes
    list_in[6] = '0'
    list_in[7] = '0'
    list_in[8] = '0'

    return list_in


def main(network_file, input_file_path, project_name, hour):
    """
    Main network parse script.
    Inputs: network_file, a d221 network file supplied as user argument.
            input_file_path, an excel file containing transit lines and
                             headways.
            project_name, the name of the project to be used for the output
                          file.
            hour, an emme hour code as user arg.
    Outputs: Single d221 batch file with edited headways and zeroed-out user
             attributes.
    """
    hour_column = 'HW_' + hour
    df = load_xlsx(input_file_path, hour_column)
    filtered_transit = filter_valid_transit(df, hour_column)

    with open(network_file, 'r') as src:
        write_line_flag = False

        filename = 'd221.' + project_name + '_' + hour

        with open(filename, 'w') as dest:
            dest.write('t lines init\n')
            dest.close()

            for line in src:

                if "a'" in line:
                    if any(transit in line for transit in filtered_transit):

                        header_list = clean_and_list(line)
                        edited_header = header_parser(header_list, hour_column,
                                                      df)

                        with open(filename, 'a') as dest:
                            str = ''
                            for item in edited_header:
                                str = str + item + '  '
                            dest.write(str + '\n')
                            write_line_flag = True
                    else:
                        write_line_flag = False

                elif write_line_flag:
                    with open(filename, 'a') as dest:
                        dest.write(line)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
