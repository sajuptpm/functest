#!/usr/bin/env python

from common import client
from common import vpc_manager
from common import utils
import netaddr
import unittest
import threading
import settings

class OverlappingVpcCidrCheck(unittest.TestCase):

    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)
	self.vpc_id = None
	
    def check_overlapping_cidr_block(self, cidr_block1, cidr_block2):
	res = self.jclient.vpc.create_vpc(cidr_block=cidr_block1)
        if res.get("Response"):
            self.assertEqual(res['Response']['Errors']['Error']['Code'],  "OverlappedVpc.Range")
            return
	self.vpc_id = res['CreateVpcResponse']['vpc']['vpcId']
	res = self.jclient.vpc.create_vpc(cidr_block=cidr_block2)
        if res.get("Response"):
            self.assertEqual(res['Response']['Errors']['Error']['Code'],  "OverlappedVpc.Range")
            return
        self.fail("Could not find expected exception OverlappedVpc.Range")

    def test_overlapping_subset_cidr(self):
	self.check_overlapping_cidr_block('11.0.0.0/16', '11.0.0.0/28')

    def test_overlapping_superset_cidr(self):
        self.check_overlapping_cidr_block('12.0.0.0/28', '12.0.0.0/16')

    def tearDown(self):
	print "......Cleaning VPC: ", self.vpc_id
	self.jclient.vpc.delete_vpc(vpc_id=self.vpc_id)

class ConcurrencyTesting(unittest.TestCase):

    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)

    def check_overlap(self):
        res = self.jclient.vpc.describe_vpcs()
        items = utils.get_item(('DescribeVpcsResponse', 'vpcSet', 'item'), res)
        cidr_blocks = [item['cidrBlock'] for item in items]
	return len(cidr_blocks) == len(set(cidr_blocks))

    def test_con(self):
        cidr_block = '11.0.0.0/16'
        net = netaddr.IPNetwork(cidr_block)
        threads = []
        for vpc_cidr in list(net.subnet(28))[:settings.VPC_QUOTA]:
	    threading.Thread(target=self.jclient.vpc.create_vpc, kwargs={'cidr_block':str(vpc_cidr)}).start() 
	self.assertTrue(self.check_overlap())

    def tearDown(self):
        self.vpc_manager.delete_all_vpcs()


if __name__ == '__main__':
    unittest.main()


