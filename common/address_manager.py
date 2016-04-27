import base_manager
import utils

class AddressManager(base_manager.BaseManager):

    def get_all_address_ids(self):
        ids = []
        items = None
        res = self.jclient.vpc.describe_addresses()
        try:
            items = utils.get_item(('DescribeAddressesResponse', 'addressesSet', 'item'), res)
        except KeyError as ex:
            pass
        if isinstance(items, list):
            return [item['allocationId'] for item in items]
        elif isinstance(items, dict):
            return [items['allocationId']]
        return ids

    def delete_all_addresses(self):
        address_ids = self.get_all_address_ids()
        print "......Cleaning Addresses: ", len(address_ids)
        for address_id in address_ids:
            self.jclient.vpc.release_address(allocation_id=address_id)

