from jcsclient import utils
from jcsclient import config
from jcsclient import exception
import json
import xmltodict
import os

def wrapper(func):
    def conv(*args, **kwargs):
        new_args = [func.__name__.replace('_', '-')]
        for (k, v,) in kwargs.items():
            new_args.extend(['--{option}'.format(option=k.replace('_', '-')), v])
        resp = func(tuple(new_args))
        if resp is not None:
            try:
                resp_dict = json.loads(resp.content)
            except:
                resp_dict = xmltodict.parse(resp.content)
                resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
                resp_dict = json.loads(resp_json)
            return resp_dict
    return conv

def getattribute(obj, name):
    attr = object.__getattribute__(obj, name)
    if callable(attr):
        attr = wrapper(attr)
    return attr

class ClientConfigHandler(config.ConfigHandler):

    def __init__(self, access_key = None, secret_key = None):
        try:
            super(ClientConfigHandler, self).__init__(None)
        except:
            pass
        #self.secure = False
        self.access_key = access_key or os.environ.get('ACCESS_KEY')
        self.secret_key = secret_key or os.environ.get('SECRET_KEY')
        if not self.access_key or not self.secret_key:
            raise exception.UnknownCredentials()

class Client(object):

    def __init__(self, access_key = None, secret_key = None):
        config.config_handler = ClientConfigHandler(access_key, secret_key)
        vpc_service_name = 'vpc'
        service = utils.load_service(vpc_service_name)
        self.vpc = utils.create_controller(service, vpc_service_name)
        self.vpc.__class__.__getattribute__ = getattribute
        compute_service_name = 'compute'
        service = utils.load_service(compute_service_name)
        self.compute = utils.create_controller(service, compute_service_name)
        self.compute.__class__.__getattribute__ = getattribute


