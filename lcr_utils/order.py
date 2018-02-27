'''
lcr (c) University of Manchester 2018

lcr is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import csv
import sys

from lcr_utils.build import BuildGenieBase


def main(args):
    '''main method.'''
    genie = BuildGenieBase({'ice': {'url': args[0],
                                    'username': args[1],
                                    'password': args[2]},
                            'ice_ids': args[3:]})

    writer = csv.writer(open('out.csv', 'w'))
    writer.writerow(['id', 'name', 'type', 'subtype', 'description',
                     'sequence'])

    for entry in genie.get_order():
        writer.writerow([str(val) if val else '' for val in entry])


if __name__ == '__main__':
    main(sys.argv[1:])
