# Eric Nordstrom

# script to confirm formatting of text data taken from drugs.com
# formatting observed upon inspection:
#   columns separated by tabs
#   first line - header
#   odd-numbered lines: rank, then drug name
#       ASSUMPTION: ranks go 1 by 1
#   even-numbered lines:
#       USUALLY company, value (sales or units), then TWO tabs, then the word Stats
#       sometimes the company name is left out, in which case THE FIRST TAB IS ALSO LEFT OUT
#       sometimes the value is left out, which does not remove a tab (this can result in 3 tabs in a row)
#       STRATEGY: count tabs FROM THE RIGHT SIDE
#
# RESULT: all datasets pass this test.


import os


def sales_path(year):
    return os.path.join('drugs.com datasets', 'raw', f'sales {year}.txt')

def units_path(year):
    return os.path.join('drugs.com datasets', 'raw', f'units {year}.txt')

def test_file(path_func, year):
    
    path = path_func(year)
    filename = os.path.split(path)[-1]
    print(f'Analyzing {filename}...')

    with open(path, 'r') as f:
        
        _ = next(f)
        even = False
        last_rank = 0

        for line in f:
            
            entries = line.split('\t')

            # test whether formatting fails
            if even and (
                entries[-1] != 'Stats\n'
                or entries[-2] != ''
                or entries[-3] and not entries[-3].replace(',', '').isnumeric()
            ) or not even and (
                not entries[0].isnumeric()
                or not entries[1].strip()  # check whether something actually included for the drug name
            ):
                print('\t' + repr(line))

            # test whether rankings are 1 by 1
            elif not even:

                rank = int(entries[0])

                if rank != last_rank + 1:
                    print(f'\t({last_rank})-->{repr(line)}')
                
                last_rank = rank

            even = not even

def main():
    for path_func in sales_path, units_path:
        for year in 2011, 2012, 2013:
            test_file(path_func, year)


if __name__ == '__main__':
    main()