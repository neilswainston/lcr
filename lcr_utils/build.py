'''
lcr (c) University of Manchester 2018

lcr is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=too-few-public-methods
import re

from synbiochem.utils.ice_utils import ICEClient
from synbiochem.utils.job import JobThread


class BuildGenieBase(JobThread):
    '''Base class for build applications.'''

    def __init__(self, query):
        JobThread.__init__(self)

        self._query = query
        self._ice_client = ICEClient(
            query['ice']['url'],
            query['ice']['username'],
            query['ice']['password'],
            group_names=query['ice'].get('groups', None))

        self._ice_ids = query['ice_ids']
        self._data = {}

    def get_order(self):
        '''Gets a plasmids constituent parts list for ordering.'''
        entries = {}

        for ice_id in self._ice_ids:
            data = self._get_data(ice_id)

            for part in data[0].get_metadata()['linkedParts']:
                data = self._get_data(part['partId'])
                entries[data[1]] = list(data[2:])

        # Format into list of lists:
        return [[key] + entries[key]
                for key in sorted(entries)]

    def _get_data(self, ice_id):
        '''Gets data from ICE entry.'''
        if ice_id in self._data:
            return self._data[ice_id]

        ice_entry = self._ice_client.get_ice_entry(ice_id)
        metadata = ice_entry.get_metadata()
        data = ice_entry, \
            metadata['partId'], \
            metadata['name'], \
            metadata['type'], \
            ice_entry.get_parameter('Type'), \
            re.sub('\\s*\\[[^\\]]*\\]\\s*', ' ',
                   metadata['shortDescription']).replace(' - ', '_'), \
            ice_entry.get_seq()

        self._data[ice_id] = data

        return data
