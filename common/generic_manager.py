import base_manager
import vpc_manager
import subnet_manager
import address_manager
import security_group_manager

class GenericManager(base_manager.BaseManager):

    def __init__(self, *args, **kwargs):
	super(GenericManager, self).__init__(*args, **kwargs)
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
	self.subnet_manager = subnet_manager.SubnetManager(self.jclient)
	self.address_manager = address_manager.AddressManager(self.jclient)
        self.security_group_manager = security_group_manager.SecurityGroupManager(self.jclient)

    def delete_vpc(self, vpc_id, force=False):
	self.subnet_manager.delete_all_subnets(vpc_id)
	self.security_group_manager.delete_all_security_groups(vpc_id)
	self.jclient.vpc.delete_vpc(vpc_id=vpc_id)
