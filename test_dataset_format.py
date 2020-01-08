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
#       company name same for all 6 datasets for a given drug name
#
# RESULT: all datasets pass this test.


import os
from drugs_tools import _path_funcs


companies = {}  # record of which company makes which drug

def test_file(path):
    
    filename = os.path.split(path)[-1]
    print(f'Analyzing {filename}...')

    with open(path, 'r') as f:
        
        _ = next(f)
        odd = True
        last_rank = 0

        for line in f:
            
            entries = line.split('\t')

            if odd:

                name = entries[1].strip()
                rank = int(entries[0])

                # check formatting
                if (
                    not entries[0].isnumeric()
                    or not name  # check whether something actually included for the drug name
                ):
                    print('\t' + repr(line))

                # checking whether ranking is 1 by 1
                if rank != last_rank + 1:
                    print(f'\t({last_rank})-->{repr(line)}')
                
                last_rank = rank

            else:
            
                company = '' if len(entries) == 3 else entries[-4]

                # check whether company is consistent
                if name in companies:
                    if companies[name] != company:
                        print(f'\t{name}: {companies[name]} or {company}?')
                else:
                    companies[name] = company

                # check formatting
                if (entries[-1] != 'Stats\n'
                    or entries[-2] != ''
                    or entries[-3] and not entries[-3].replace(',', '').isnumeric()
                ):
                    print('\t' + repr(line))

            odd = not odd

def main():
    for value_type in 'sales', 'units':
        for year in 2011, 2012, 2013:
            test_file(_path_funcs['in'][value_type](year))


if __name__ == '__main__':
    main()