
#####How to use it ?
        
#####Install jcsclient
        $git clone https://github.com/jiocloudservices/jcsclient
        $cd jcsclient
        $python setup.py develop
#####Export credentials

        export ACCESS_KEY=xxxxxxxxxx
        export SECRET_KEY=xxxxxxxxxx
        export VPC_URL="https://network.jiocloud.com/"
        export COMPUTE_URL="http://compute.jiocloud.com:8788"

#####Clone this repo

        $git clone https://github.com/JioCloudVPC/scripts
        $cd scripts/functest

#####Example-1
        from common import client
        self.jclient = client.Client()
        self.jclient.vpc.create_vpc(cidr_block='10.0.0.0/16')
        self.jclient.vpc.describe_vpcs()
        self.jclient.compute.describe_instances()
        
#####Example-2
        from common import client
        self.jclient = client.Client(access_key=xxxx, secret_key=xxxx)
        self.jclient.vpc.create_vpc(cidr_block='10.0.0.0/16')
        self.jclient.vpc.describe_vpcs()
        self.jclient.compute.describe_instances()

