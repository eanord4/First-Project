# tools for processing drugs.com data from preprocessed .csv files


import os
import pandas as pd


# for preprocessing
_indir = 'drugs.com-datasets-original'
_outdir = 'drugs.com-datasets-preprocessed'
_path_funcs = {

    'in': {
        'sales': lambda year: os.path.join(_indir, f'sales {year}.txt'),
        'units': lambda year: os.path.join(_indir, f'units {year}.txt')
    },

    'out': {
        'sales': lambda year: os.path.join(_outdir, f'sales {year}.csv'),
        'units': lambda year: os.path.join(_outdir, f'units {year}.csv')
    }

}


# for getting data file paths
sales_path = _path_funcs['out']['sales']
units_path = _path_funcs['out']['units']

