import base_manager
import generic_manager
import utils

class VpcManager(base_manager.BaseManager):

    def create_vpc(self, cidr_block):
        res = self.jclient.vpc.create_vpc(cidr_block=cidr_block)
        vpc_id = utils.get_item(('CreateVpcResponse', 'vpc', 'vpcId'), res)
        return vpc_id

    def get_all_vpc_ids(self):
        ids = []
        items = None
        res = self.jclient.vpc.describe_vpcs()
        try:
            items = utils.get_item(('DescribeVpcsResponse', 'vpcSet', 'item'), res)
        except KeyError as ex:
            pass
        if isinstance(items, list):
            return [item['vpcId'] for item in items]
        elif isinstance(items, dict):
            return [items['vpcId']]
        return ids

    def delete_all_vpcs(self, force=False):
        vpc_ids = self.get_all_vpc_ids()
        print "......Cleaning VPCs: ", len(vpc_ids)
        for vpc_id in vpc_ids:
	    if force:
		gm = generic_manager.GenericManager(self.jclient)
		gm.delete_vpc(vpc_id)
	    else:
            	self.jclient.vpc.delete_vpc(vpc_id=vpc_id)

