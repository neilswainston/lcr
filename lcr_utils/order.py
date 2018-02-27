'''
lcr (c) University of Manchester 2018

lcr is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import sys

from lcr_utils.build import BuildGenieBase


def main(args):
    '''main method.'''
    genie = BuildGenieBase({'ice': {'url': args[0],
                                    'username': args[1],
                                    'password': args[2]},
                            'ice_ids': args[3:]})

    entries = genie.get_order()

    with open('out.txt', 'w') as out:
        out.write('\t'.join(['id', 'name', 'type', 'subtype', 'description',
                             'sequence']))
        out.write('\n')

        for entry in entries:
            out.write('\t'.join([str(val) if val else '' for val in entry]))
            out.write('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
