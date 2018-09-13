"""
24_hr_d221_split.py

Reads d221 files and creates separate text files per transit line.
"""


import sys
import os
import pandas as pd
import re


def load_xlsx(hour_in):
    xlsx_file = os.path.abspath(
        'H:/rtp/2018rtp/_round2/modelRuns/2015/development/'
        'Inputs_2015_Kate_DEV.xlsx')
    df_transit_lines = pd.read_excel(xlsx_file, sheet_name='transit_lines')
    df_transit_types = pd.read_excel(xlsx_file, sheet_name='transit_types')
    df_joined = pd.merge(df_transit_lines, df_transit_types, on='TRIMET_TYPE')
    return df_joined


def filter_valid_transit(df_in, hour_in):
    df_in = df_in[df_in[hour_in].notnull()]
    transit_list = df_in['VEH_ID'].tolist()
    return transit_list


def clean_and_list(header_in):
    """Converts raw text lines to cleaned lists.
    Input: header_in, the header line.
    """
    # list everything between single quotes, e.g. 'BLUE    HILLS/GRESHa  '
    list_match = re.findall(r"'(.*?)'", header_in)
    stripped_id = list_match[0].strip()
    stripped_name = ' '.join(list_match[1].split())
    header_in = header_in.replace(list_match[0], stripped_id)
    header_in = header_in.replace(list_match[1], stripped_name)
    return filter(None, header_in.rstrip().split(' '))


def header_parser(list_in):
    """
    hour is time of day `HW_0001`, etc.
    """
    
    #list_in[0] = "a'" + list_in[0]
    #list_in[3] = 

    return list_in
    

def main(network_file, hour):
    """
    Main network parse script.
    inputs: network_file,  a d221 network file supplied as user argument.
    """
    df = load_xlsx(hour)
    filtered_transit = filter_valid_transit(df, hour)
    
    with open(network_file, 'r') as src:
        write_line_flag = False

        for line in src:
                        
            if "a'" in line:
                if any(transit in line for transit in filtered_transit):

                    filename = line[:8].replace(' ', '')
                    filename = filename.replace("'", '')
                    filename = filename[1:] + '.txt'

                    header_list = clean_and_list(line)
                    print header_list
                    edited_header = header_parser(header_list)

                    with open(filename, 'w') as dest:
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
    main(sys.argv[1], sys.argv[2])
