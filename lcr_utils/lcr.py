'''
lcr (c) University of Manchester 2018

lcr is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=too-many-arguments
import sys

from lcr_utils.assembly import AssemblyThread, _AMPLIGASE, _LCR_MASTERMIX, \
    _WATER


class LcrThread(AssemblyThread):
    '''Class implementing AssemblyGenie algorithms.'''

    def run(self):
        '''Exports recipes.'''
        pools = self._get_pools()

        # Write plates:
        self._comp_well.update(self._write_plate('MastermixTrough',
                                                 [[_WATER],
                                                  [_LCR_MASTERMIX]]))

        self._comp_well.update(self._write_plate('components',
                                                 self.get_order()
                                                 + [[_AMPLIGASE]]))

        # Write domino pools worklist:
        self._comp_well.update(
            self._write_dom_pool_worklist(pools, 'domino_pools', 1.75))

        # Write LCR worklist:
        self.__write_lcr_worklist('lcr', pools)

    def __write_lcr_worklist(self, dest_plate_id, pools):
        '''Writes LCR worklist.'''
        self._write_worklist_header(dest_plate_id)

        def_reagents = {_LCR_MASTERMIX: 7.0, _AMPLIGASE: 1.5}

        # Write water (special case: appears in many wells to optimise
        # dispensing efficiency):
        part_vol = 1
        self.__write_water_worklist(dest_plate_id, pools, 15.5, part_vol)
        self.__write_parts_worklist(dest_plate_id, pools, part_vol)
        self.__write_dom_pools_worklist(dest_plate_id, 1)
        self.__write_default_reag_worklist(dest_plate_id, def_reagents)

    def __write_water_worklist(self, dest_plate_id, pools, total, part_vol):
        '''Write water worklist.'''
        worklist = []

        for dest_idx, ice_id in enumerate(self._ice_ids):
            well = self._comp_well[_WATER][dest_idx]

            h2o_vol = total - \
                (len(pools[ice_id]['backbone']) +
                 len(pools[ice_id]['parts'])) * part_vol

            # Write water:
            worklist.append([dest_plate_id, dest_idx, well[1],
                             well[0], str(h2o_vol),
                             _WATER, _WATER, '',
                             ice_id])

        self._write_worklist(dest_plate_id, worklist)

    def __write_parts_worklist(self, dest_plate_id, pools, part_vol):
        '''Write parts worklist.'''
        worklist = []

        for dest_idx, ice_id in enumerate(self._ice_ids):
            # Write backbone:
            for comp in pools[ice_id]['backbone']:
                well = self._comp_well[comp[1]]

                worklist.append([dest_plate_id, dest_idx, well[1],
                                 well[0], str(part_vol),
                                 comp[2], comp[5], comp[1],
                                 ice_id])

            # Write parts:
            for comp in pools[ice_id]['parts']:
                well = self._comp_well[comp[1]]

                worklist.append([dest_plate_id, dest_idx, well[1],
                                 well[0], str(1),
                                 comp[2], comp[5], comp[1],
                                 ice_id])

        self._write_worklist(dest_plate_id, worklist)

    def __write_dom_pools_worklist(self, dest_plate_id, vol):
        '''Write domino pools worklist.'''
        worklist = []

        for dest_idx, ice_id in enumerate(self._ice_ids):
            well = self._comp_well[ice_id + '_domino_pool']

            worklist.append([dest_plate_id, dest_idx, well[1],
                             well[0], str(vol),
                             'domino pool', 'domino pool', '',
                             ice_id])

        self._write_worklist(dest_plate_id, worklist)

    def __write_default_reag_worklist(self, dest_plate_id, def_reagents):
        '''Write default reagents worklist.'''
        worklist = []

        for dest_idx, ice_id in enumerate(self._ice_ids):
            for reagent, vol in def_reagents.iteritems():
                well = self._comp_well[reagent]

                worklist.append([dest_plate_id, dest_idx, well[1],
                                 well[0], str(vol),
                                 reagent, reagent, '',
                                 ice_id])

        self._write_worklist(dest_plate_id, worklist)


def main(args):
    '''main method.'''
    thread = LcrThread({'ice': {'url': args[0],
                                'username': args[1],
                                'password': args[2]},
                        'ice_ids': args[3:]})

    thread.run()


if __name__ == '__main__':
    main(sys.argv[1:])
