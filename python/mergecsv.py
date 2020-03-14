import numpy as np
from astropy.table import Table, vstack
from astropy.io.ascii import convert_numpy

# Manually taken from
# http://www.stsci.edu/stsci-research/research-topics-and-programs/ullyses/target-tables
tabnames = ['cha-1', 'CrA', 'eps-cha', 'eta-cha', 'lupus', 'orion-ob1',
            'sigma-ori', 'tw-hydrae-association']

url = 'http://www.stsci.edu/files/live/sites/www/files/home/stsci-research/research-topics-and-programs/ullyses/target-tables/_documents/'

# Define converter for "AR modes"  otherwise it is read as int64 if empty
# and then I can't merge tables later because they have different types
tablist = [Table.read(url + t + '.csv',
                      converters={'AR modes': [convert_numpy(np.str)]})
           for t in tabnames]

# The table of monitoring targets has very different format.
# Hand-edited file fixes some of that,
# the rest is done below.
tabnames.append('monitor')
tab = Table.read('classical-t-tauri-star-monitoring-targets.csv',
                          converters={'AR modes': [convert_numpy(np.str)]})
tab['log(dm/dt)'] = np.log10(tab['Massaccrate'])
tab.remove_column('Massaccrate')
tablist.append(tab)

# Add column with region
for t, n in zip(tablist, tabnames):
    t['region'] = n

tabctts = vstack(tablist)
tabctts.write('../mergedCTTSlist.csv', overwrite=True)
