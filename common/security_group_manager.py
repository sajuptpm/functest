import base_manager
import utils

class SecurityGroupManager(base_manager.BaseManager):

    def get_all_security_group_ids(self, vpc_id, include_default_group=False):
        ids = []
        items = None
        res = self.jclient.vpc.describe_security_groups()
        try:
            items = utils.get_item(('DescribeSecurityGroupsResponse', 'securityGroupInfo', 'item'), res)
        except KeyError as ex:
            pass
        if isinstance(items, list):
	    if include_default_group:
		return [item['groupId'] for item in items if item.get('vpcId') == vpc_id]
	    else:
            	return [item['groupId'] for item in items if item.get('vpcId') == vpc_id if item.get('groupName') != 'default']
        elif isinstance(items, dict):
	    if include_default_group:
		if items['vpcId'] == vpc_id:
		    return [items['groupId']]
	    else:
		if items['vpcId'] == vpc_id and items.get('groupName') != 'default':
            	    return [items['groupId']]
        return ids

    def delete_all_security_groups(self, vpc_id, include_default_group=False):
        ids = self.get_all_security_group_ids(vpc_id, include_default_group=include_default_group)
        print "......Cleaning Security Groups: ", len(ids)
        for secgrp_id in ids:
            self.jclient.vpc.delete_security_group(group_id=secgrp_id)


