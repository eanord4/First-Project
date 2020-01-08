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
YEARS = (2011, 2012, 2013)


# for getting data frames
def dataframe(value_types, years, dropna=True, companies=False):
    """import the data of the value type(s) ('sales' and/or 'units') from the given year(s) (2011 thru 2013, inner-joined) as a data frame, with totals column(s) if `years` is iterable"""

    # interpret `value_types`
    if isinstance(value_types, str):
        if value_types == 'both':
            return dataframe(['units', 'sales'], years, dropna, companies)
        value_type = value_types
    else:
        if len(value_types) == 2:
            return dataframe(value_types[0], years, dropna, companies)\
                .merge(dataframe(value_types[1], years, dropna, companies=False), left_index=True, right_index=True)
        # assume len = 1
        value_type = value_types[0]

    # interpret `years`
    if '__iter__' in dir(years):
        # iterable
        years = list(years)
        sum = True
    else:
        # not iterable
        years = [years]
        sum = False
    
    # interpret `companies`
    if companies:
        co_func = lambda years: pd.read_csv(_path_funcs['out'][value_type](years[0])).set_index('name')
    else:
        co_func = lambda years: pd.read_csv(_path_funcs['out'][value_type](years[0])).set_index('name').drop('company', 1)

    # interpret `dropna`
    if dropna:
        next_df = lambda years: co_func(years).dropna()
    else:
        next_df = lambda years: co_func(years)

    # initialize
    df = next_df(years)
    co_func = lambda years: pd.read_csv(_path_funcs['out'][value_type](years[0])).set_index('name').drop('company', 1)

    # join
    while len(years) > 1:
        suffixes = '_' + str(years.pop(0)), '_' + str(years[0])
        df = df.merge(
            next_df(years),
            left_index=True,
            right_index=True,
            suffixes=suffixes
        )
    
    if sum:
        # assign totals column
        if value_type == 'sales':
            return df.assign(total_sales_MM=lambda x: x.sum(1))
        return df.assign(total_units_MM=lambda x: x.sum(1))
    return df
