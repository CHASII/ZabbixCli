'''
Author: Chas
LastEditors: Chas
Version: 
Description: 
'''
import random
import argparse

# Import Custom Model
from app import api as zbx
from conf import settings as set

class ZBXCLI(object):

	def __init__(self):
		self.zbx_token = zbx.AUTH().getToken()

	def randomColor(self):
		return ("".join(random.choice("0123456789ABCDEF") for i in range(6)))

	def handleItem(self, key, hosts):
		items = []
		for host in hosts:
			items.append(zbx.ITEM(self.zbx_token).getItemID(host, key)[0]["itemid"])
		return items

	def handleHost(self, hosts):
		items = self.handleItem(args.key, hosts)
		self.createGraph(items)

	def handleGroup(self, groups):
		for group in groups:
			result = zbx.HOSTGROUP(self.zbx_token).getGroupID(group)
			if(result):
				hosts = zbx.HOST(self.zbx_token).getHostID(result[0]["groupid"])
				hostnames = [h["host"] for h in hosts]
				set.logger.info(f"\"{group}\" includes these hosts: " + ",".join(hostnames))
				items = self.handleItem(args.key, hostnames)
				self.createGraph(items)
			else:
				set.logger.warning(f"\"{group}\" not includes any host")

	def createGraph(self, items):
		gitems = []
		for id in items:
			gitems.append({"itemid":id, "color": self.randomColor()})
		set.logger.info(zbx.GRAPH(self.zbx_token).createGrapth(args.name, set.Zabbix["gwidth"], set.Zabbix["gheight"], gitems))

parser = argparse.ArgumentParser(description=f"=== Zabbix Cli ===")
parser.add_argument("-key", required=True, type=str, help="Zabbix Item Key")
parser.add_argument("-name", required=True, type=str, help="Zabbix Graph Name")
parser.add_argument("-type", required=True, type=str, choices=["hostgraph","groupgraph"])
parser.add_argument('-nargs', required=True, nargs='+',help="Support Hosts and HostGroups, like 'host1' 'host2' or 'group1' 'gooup2'")
args = parser.parse_args()

if args:
	if args.type == "hostgraph":
		ZBXCLI().handleHost(args.nargs)
	elif args.type == "groupgraph":
		ZBXCLI().handleGroup(args.nargs)
	else:
		print("Error Args,You Should Run With: python3 ./main.py -h")
