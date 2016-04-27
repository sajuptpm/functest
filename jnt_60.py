import client
import unittest
import netaddr

VPC_QUOTA = 11
SUBNET_QUOTA = 30
ADDRESS_QUOTA = 10

class VpcQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()

    def get_all_vpc_ids(self):
        vpc_ids = []
        res = self.jclient.vpc.describe_vpcs()
        try:
            vpcs = res['DescribeVpcsResponse']['vpcSet']['item']
        except KeyError as ex:
            pass
        if isinstance(vpcs, list):
            return [vpc['vpcId'] for vpc in vpcs]        
        elif isinstance(vpcs, dict):
            return [vpcs['vpcId']]
        return vpc_ids

    def clear_all_vpcs(self):
        vpc_ids = self.get_all_vpc_ids()
        print "......Cleaning VPCs: ", len(vpc_ids)
        for vpc_id in vpc_ids:
            self.jclient.vpc.delete_vpc(vpc_id=vpc_id)

    def test_vpc_quota(self):
	for x in range(VPC_QUOTA):
            res = self.jclient.vpc.create_vpc(cidr_block='10.0.0.0/16')
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "VpcLimitExceeded")
                return
        self.fail("Could not find expected exception VpcLimitExceeded")

    def tearDown(self):
        self.clear_all_vpcs()

class SubnetQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.vpc_id = None

    def create_vpc(self, cidr_block):
        res = self.jclient.vpc.create_vpc(cidr_block=cidr_block)
        vpc_id = res['CreateVpcResponse']['vpc']['vpcId']
        return vpc_id

    def get_all_subnet_ids(self):
        subnet_ids = []
        res = self.jclient.vpc.describe_subnets()
        try:
            subnets = res['DescribeSubnetsResponse']['subnetSet']['item']
        except KeyError as ex:
            pass
        if isinstance(subnets, list):
            return [subnet['subnetId'] for subnet in subnets if subnet['vpcId']==self.vpc_id]
        elif isinstance(subnets, dict):
            if subnets['vpcId'] == self.vpc_id:
                return [subnets['subnetId']]
        return subnet_ids

    def clear_all_subnets(self):
        subnet_ids = self.get_all_subnet_ids()
        print "......Cleaning Subnets: ", len(subnet_ids)
        for subnet_id in subnet_ids:
            self.jclient.vpc.delete_subnet(subnet_id=subnet_id)

    def test_subnet_quota(self):
        cidr_block = '10.0.0.0/16'
        self.vpc_id = self.create_vpc(cidr_block)
        net = netaddr.IPNetwork(cidr_block)
        for subnet_cidr in list(net.subnet(28))[:SUBNET_QUOTA]:
            res = self.jclient.vpc.create_subnet(vpc_id=self.vpc_id, cidr_block=str(subnet_cidr))
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "SubnetLimitExceeded")
                return
        self.fail("Could not find expected exception SubnetLimitExceeded")

    def tearDown(self):
        self.clear_all_subnets()

class AddressQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()

    def get_all_address_ids(self):
        address_ids = []
        res = self.jclient.vpc.describe_addresses()
        try:
            addresses = res['DescribeAddressesResponse']['addressesSet']['item']
        except KeyError as ex:
            pass
        if isinstance(addresses, list):
            return [address['allocationId'] for address in addresses]
        elif isinstance(addresses, dict):
            return [addresses['allocationId']]
        return address_ids

    def clear_all_addresses(self):
        address_ids = self.get_all_address_ids()
        print "......Cleaning Addresses: ", len(address_ids)
        for address_id in address_ids:
            self.jclient.vpc.release_address(allocation_id=address_id)
           
    def test_address_quota(self):
        for x in range(ADDRESS_QUOTA):
            res = self.jclient.vpc.allocate_address(domain='vpc')
            if res.get("Response"):
		self.assertEqual(res['Response']['Errors']['Error']['Code'],  "AddressLimitExceeded")
                return
        self.fail("Could not find expected exception AddressLimitExceeded")
 
    def tearDown(self):
        self.clear_all_addresses()


if __name__ == '__main__':
    unittest.main()

