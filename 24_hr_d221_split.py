"""
24_hr_d221_split.py

Reads d221 files and creates separate text files per transit line.
"""


import sys


def main(network_file):
    """
    Main network parse script.
    inputs: network_file,  a user argument.
    """
    with open(network_file, 'r') as src:
        write_line_marker = False

        for line in src:
            if "a'" in line:
                filename = line[:8].replace(' ', '')
                filename = filename.replace("'", '')
                filename = filename[1:] + '.txt'
                with open(filename, 'w') as dest:
                    dest.write(line)
                    write_line_marker = True

            elif write_line_marker:
                with open(filename, 'a') as dest:
                    dest.write(line)

if __name__ == '__main__':
    main(sys.argv[1])
