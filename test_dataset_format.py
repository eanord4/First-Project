# script to convert raw text datasets from drugs.com into csv

import os, csv

sales_base_path = os.path.join('drugs.com datasets', 'raw', 'sales ')
units_base_path = os.path.join('drugs.com datasets', 'raw', 'units ')

with open(sales_base_path + '2013.txt', 'r') as f:

    header = next(f)
    even = False

    for line in f:
        
        tab_indices = []

        for i, char in enumerate(line):
            if char == '\t':
                tab_indices.append(i)
        
        # confirm characteristics of odd and even lines
        if even and (
            len(tab_indices) != 3
            or tab_indices[1] != tab_indices[2] - 1  # 2nd and 3rd tabs adjacent
            or 
        ):

        even = not even