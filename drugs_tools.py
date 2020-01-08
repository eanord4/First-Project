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


# for getting data frames

def dataframe(value_type, years, dropna=True):
    """import the data of the value type ('sales' or 'units') from the given year(s) (2011 thru 2013, inner-joined) as a data frame, with totals column if iterable"""

    if '__iter__' in dir(years):
        # iterable
        years = list(years)
        sum = True
    else:
        # not iterable
        years = [years]
        sum = False

    if dropna:
        next_df = lambda years: pd.read_csv(_path_funcs['out'][value_type](years[0])).set_index('name').dropna()
    else:
        next_df = lambda years: pd.read_csv(_path_funcs['out'][value_type](years[0])).set_index('name')

    df = next_df(years)

    while len(years) > 1:
        suffixes = '_' + str(years.pop(0)), '_' + str(years[0])
        df = df.merge(
            next_df(years),
            on='name',
            suffixes=suffixes
        )
    
    if sum and value_type == 'sales':
        return df.assign(total_sales_1000s=lambda x: x.sum(1))
    return df
