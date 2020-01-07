# Eric Nordstrom

# script to convert raw text datasets from drugs.com into csv
# formatting assumptions tested via test_dataset_format.py, found in the `test` branch of this repo


import os, csv


indir = 'drugs.com-datasets-original'
outdir = 'drugs.com-datasets-preprocessed'
path_funcs = {

    'in': {
        'sales': lambda year: os.path.join(indir, f'sales {year}.txt'),
        'units': lambda year: os.path.join(indir, f'units {year}.txt')
    },

    'out': {
        'sales': lambda year: os.path.join(outdir, f'sales {year}.csv'),
        'units': lambda year: os.path.join(outdir, f'units {year}.csv')
    }

}


def process_file(value_type, year):

    inpath = path_funcs['in'][value_type](year)
    outpath = path_funcs['out'][value_type](year)
    infilename = os.path.split(inpath)[-1]
    outfilename = os.path.split(outpath)[-1]
    print(f'Processing {infilename} to {outfilename}...')

    with open(inpath, 'r') as infile, open(outpath, 'w') as outfile:
        
        odd = True
        _ = next(infile)
        writer = csv.writer(outfile)
        writer.writerow([
            'name',
            'company',
            value_type + '_thousands'  # both sales and units are given in thousands
        ])  # header of output file

        for inline in infile:
            
            if odd:
                last_odd = inline.split('\t')
            else:
                last_even = inline.split('\t')
                writer.writerow([
                    last_odd[1].rstrip(),  # drug name
                    last_even[-4] if len(last_even) > 3 else '',  # company
                    last_even[-3].replace(',', '')  # value
                ])

            odd = not odd

def main():
    for value_type in 'sales', 'units':
        for year in 2011, 2012, 2013:
            process_file(value_type, year)


if __name__ == '__main__':
    main()