"""
Author: Chas
LastEditors: Chas
Version: 
Description: 
"""
import requests
import json
import urllib3
urllib3.disable_warnings()

# Import Custom Model
from conf import settings as set


class AUTH(object):

    def __init__(self):
        self.zabbix_api = set.Zabbix["api"]
        self.zabbix_user = set.Zabbix["user"]
        self.zabbix_pass = set.Zabbix["pass"]
        
    def rpcResult(self, params):
        headers = {"Content-Type": "application/json-rpc"}
        rsp = requests.post(url=self.zabbix_api, headers=headers, data=json.dumps(params))
        try:
            return rsp.json()["result"]
        except:
            set.logger.error(rsp.json()["error"])
            exit(1)

    def getCookies(self):
        params = {
            "name": set.Zabbix["user"],
            "password": set.Zabbix["pass"],
            "enter": "Sign in"
        }
        rep = requests.post("/".join(set.Zabbix["api"].split("/")[:-1]) +"/index.php?login=1/", data=params)
        return rep.cookies

    def getToken(self):
        params = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.zabbix_user,
                "password": self.zabbix_pass,
            },
            "id": 1
        }
        return self.rpcResult(params)
    
    def destroyToken(self, token):
        params = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": [],
            "auth": token,
            "id": 1
        }
        return self.rpcResult(params)


class HOST(object):
    
    def __init__(self, zbx_token):
        self.zbx_token = zbx_token

    def getHostID(self, groupid):
        params = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid","host"],
                "groupids": groupid
            },
            "auth": self.zbx_token,
            "id": 1
        }
        return AUTH().rpcResult(params)

class HOSTGROUP(object):

    def __init__(self, zbx_token):
        self.zbx_token = zbx_token

    def getGroupID(self, hostgroup):
        params = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "groupid",
                "filter": {
                    "name": [hostgroup]
                }
            },
            "auth": self.zbx_token,
            "id": 1
        }
        return AUTH().rpcResult(params)


class ITEM(object):

    def __init__(self, zbx_token):
        self.zbx_token = zbx_token

    def getItemID(self, host, key):
        params = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "itemid",
                "host": host,
                "search": {
                    "key_": key
                },
            },
            "auth": self.zbx_token,
            "id": 1
        }
        return AUTH().rpcResult(params)


class GRAPH(object):

    def __init__(self, zbx_token):
        self.zbx_token = zbx_token

    def createGrapth(self, gname, gwidth, gheight, gitems):
        params = {
            "jsonrpc": "2.0",
            "method": "graph.create",
            "params": {
                "name": gname,
                "width": gwidth,
                "height": gheight,
                "gitems": gitems
            },
            "auth": self.zbx_token,
            "id": 1
        }
        return AUTH().rpcResult(params)
