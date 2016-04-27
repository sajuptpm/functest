#!/usr/bin/env python

from common import client
from common import vpc_manager
from common import subnet_manager
from common import address_manager
import unittest
import netaddr
import settings

class VpcQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
	self.vpc_manager = vpc_manager.VpcManager(self.jclient)

    def test_vpc_quota(self):
	cidr_block = '11.0.0.0/16'
        net = netaddr.IPNetwork(cidr_block)
        for vpc_cidr in list(net.subnet(28))[:settings.VPC_QUOTA+1]:
            res = self.jclient.vpc.create_vpc(cidr_block=str(vpc_cidr))
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "VpcLimitExceeded")
                return
        self.fail("Could not find expected exception VpcLimitExceeded")

    def tearDown(self):
        self.vpc_manager.delete_all_vpcs()

class SubnetQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
	self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.subnet_manager = subnet_manager.SubnetManager(self.jclient)
        self.vpc_id = None

    def test_subnet_quota(self):
        cidr_block = '12.0.0.0/16'
        self.vpc_id = self.vpc_manager.create_vpc(cidr_block)
        net = netaddr.IPNetwork(cidr_block)
        for subnet_cidr in list(net.subnet(28))[:settings.SUBNET_QUOTA+1]:
            res = self.jclient.vpc.create_subnet(vpc_id=self.vpc_id, cidr_block=str(subnet_cidr))
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "SubnetLimitExceeded")
                return
        self.fail("Could not find expected exception SubnetLimitExceeded")

    def tearDown(self):
        self.subnet_manager.delete_all_subnets(self.vpc_id)

class AddressQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.address_manager = address_manager.AddressManager(self.jclient)

    def test_address_quota(self):
        for x in range(settings.ADDRESS_QUOTA+1):
            res = self.jclient.vpc.allocate_address(domain='vpc')
            if res.get("Response"):
		self.assertEqual(res['Response']['Errors']['Error']['Code'],  "AddressLimitExceeded")
                return
        self.fail("Could not find expected exception AddressLimitExceeded")
 
    def tearDown(self):
        self.address_manager.delete_all_addresses()


if __name__ == '__main__':
    unittest.main()

