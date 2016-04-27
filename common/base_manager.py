import client
import unittest

class BaseManager(object):
    def __init__(self, client):
        self.jclient = client
	
