

def get_item(keys, _dict):
    res_dict = dict(_dict)
    for k in keys:
	if res_dict:
	    res_dict = res_dict.get(k)
    return res_dict
