# Eric Nordstrom

# script to convert raw text datasets from drugs.com into csv
# formatting assumptions tested via test_dataset_format.py, found in the `test` branch of this repo


import os, csv
from drugs_tools import _path_funcs


def process_file(value_type, year):

    inpath = _path_funcs['in'][value_type](year)
    outpath = _path_funcs['out'][value_type](year)
    infilename = os.path.split(inpath)[-1]
    outfilename = os.path.split(outpath)[-1]
    print(f'Processing "{infilename}" to "{outfilename}"...')

    with open(inpath, 'r') as infile, open(outpath, 'w') as outfile:
        
        odd = True
        _ = next(infile)
        writer = csv.writer(outfile)
        writer.writerow([
            'name',
            'company',
            value_type + '_MM'  # both sales and units are given in thousands; to be converted to millions for readability
        ])  # header of output file

        for line in infile:
            
            if odd:
                last_odd = line.split('\t')
            else:

                last_even = line.split('\t')
                value = last_even[-3].replace(',', '')
                
                if value:
                    value = int(value) / 1000

                writer.writerow([
                    last_odd[1].rstrip(),  # drug name
                    last_even[-4] if len(last_even) > 3 else '',  # company
                    value  # convert from thousands to millions
                ])

            odd = not odd

def main():
    for value_type in 'sales', 'units':
        for year in 2011, 2012, 2013:
            process_file(value_type, year)


if __name__ == '__main__':
    main()