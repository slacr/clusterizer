"""
Execnettle is a hostfinding script that dynamically queries the network. 




TODO

"""


import execnet, Queue, threading, nmap, time, sys, remote1, logging

class Execnettle(object):

	def __init__(self, nodemax=20):
		"""
		nodemax: the number of nodes you need at any one time.

		Returns nothing.
		"""
		self._nodemax = nodemax
		self._getq = None
		self._remq = None
		self._farmer = None
		self._butcher = None
		self._xfarmer = threading.Event()
		self._xbutcher = threading.Event()
		self.initnettle()

	def initnettle(self):
		"""
		The initialization method for an Execnettle object.

		Returns nothing.
		"""
		if self._getq or self._remq or self._farmer or self._butcher:
			print("you can only init once")
			return -1
		self._getq = Queue.Queue(self.nodemax)
		self._remq = Queue.Queue()
		self._farmer = execnettle.startthread(self, execnettle.harvestnodes)
		self._butcher = execnettle.startthread(self, execnettle.slaughternodes)

	def gethost(self, src="", **kwargs):
		"""
		If the node list is empty or more nodes than are available 
		were requested, gethost returns -1

		Returns the execnet gateway on success, -1 otherwise.
		"""
		if src == "": return -1
		try: gate = self._getq.get(True)
		except Queue.Empty:
			print("checking threads")
			execnettle.checkthreads(self)
			return -1
		try: return execnet.makegateway("ssh=ramphi10@"+gate).remote_exec(src, **kwargs)
		except execnet.gateway.HostNotFound:
			return self.gethost(src, **kwargs)

	def killhost(self, host):
		"""
		Disconnect from a host.

		For now we just give the slaughternode thread something to do
		but this func should be where any userland closes happen.

		Returns nothing.
		"""
		self._remq.put(host, True) 

	def termnettle(self)
		print("setting farmer lock")
		self._xfarmer.set()

		print("setting butcher lock")
		self._xbutcher.set()
		
		self._farmer.join()
		self._butcher.join()

##
##-------------Static Methods-------------------
##

	@staticmethod
	def startthread(self, sauce, daemon=False):
		t = threading.Thread(target=sauce, args=(self,))
		t.daemon=daemon
		t.start()
		return t

	@staticmethod
	def checkthreads(self):
		if not self._farmer.is_alive():
			if self._xfarmer.is_set():
				self._xfarmer.clear()
			self._farmer = startthread(harvestnodes)
		if not self._butcher.is_alive():
			if self._xbutcher.is_set():
						self._xbutcher.clear()
			self._butcher = startthread(slaughternodes)

	@staticmethod
	def slaughternodes(self):
		while not self._xfarmer.is_set():
			try:
				rem = self._remq.get(True, 2)
			except Queue.Empty:
				continue
			if rem != None:
				rem.close()
		print("watsoup indeed")
		

	@staticmethod
	def harvestnodes(self):
		nm = nmap.PortScanner()
		while not self._xbutcher.is_set():
			nm.scan(hosts='10.14.20.0/24', arguments='-p 22')
##			map(lambda x: self._getq.put(x, True, 4), map( \
##					lambda x: nm[x]['tcp'][22]['state'] or x, nm.all_hosts()))

			for h in nm.all_hosts():
				if self._xbutcher.is_set():
					break
				if nm[h]['tcp'][22]['state'] == 'open':
					try:
						self._getq.put(h, True, 1)
					except Queue.Full:
						continue
		print("doodwatsoupppppp")

## our testing class
class testexecnettle(execnettle):
	def __init__(self, nodemax):
		self.nodemax = nodemax
		super(testexecnettle, self).__init__(nodemax)

	def watwegot(self):
		print("***********watwegot**************")
		print("we've gota farmer named "+ self._farmer.name)
		print("and a butcher named "+self._butcher.name)
		print("a getq of size " +str(self._getq.qsize()))
		print("a remq of size "+str(self._remq.qsize()))
		print("***********watwegot**************")

def multiplier(channel, factor):
	while not channel.isclosed():
		param = channel.receive()
		channel.send(param * factor)

if __name__=='__main__':
	t = testexecnettle(4)

	print("testing execnettle")
	t.initnettle()
	t.watwegot()

	print("****** testing inline execs *****")
	p = t.gethost("channel.send(channel.receive()+1)")
	p.send(1)
	print("inline exec got this: "+str(p.receive()))
	print("****** inlines worked gooooood ******")

	print("****** testing pure function execs ******")
	p = []
	for i in range(2):
		p.append(t.gethost(multiplier, factor=4))
		p[i].send(i)
		print("got factor: "+str(p[i].receive()))
	t.watwegot()
	for i in range(2):
		t.killhost(p[i])
	t.watwegot()
	print("******** pure functions worked good *******")

	print("******** testing module execs ***********")
	p = t.gethost(remote1)
	print("p.receive()")
	print("********* modules worked good ************")
	time.sleep(3)
	t.watwegot()
	t.termnettle()
	
