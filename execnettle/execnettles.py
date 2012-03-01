"""
Execnettle is a hostfinding script that dynamically queries the network and
creates/retrieves new execnet gateways to hosts on the cluster for you.

NOTES
* Maybe we don't need an entire nmap plugin. We can just have a very short bash
script that python calls, and we can awk the output or parse xml. (j)

TODO
* Get constructor running.

"""

import execnet, Queue, threading, nmap, logging, sys

"""
Log all logging.info('wat') messages to logs/execnettles.log
"""
logging.basicConfig(filename='logs/execnettles.log',level=logging.DEBUG)

class Execnettle(object):

	def __init__(self, nodemax=20):
		"""
		nodemax: the number of nodes you need at any one time.
		"""
		self._nodemax = nodemax
		self._getq = None
		self._remq = None
		self._farmer = None
		self._butcher = None
		self._xfarmer = threading.Event()
		self._xbutcher = threading.Event()
		logging.info("Successfully initialized fields")
		self.initialize()

	def initialize(self):
		"""
		The initialization method for an Execnettle object.

		Returns nothing.
		"""
		if self._getq or self._remq or self._farmer or self._butcher:
			logging.error("Previously initialized")
			return -1
		self._getq = Queue.Queue(self._nodemax)
		self._remq = Queue.Queue()
		self._farmer = Execnettle.startthread(self, Execnettle.harvestnodes)
		self._butcher = Execnettle.startthread(self, Execnettle.slaughternodes)

	def gethost(self, src="", **kwargs):
		"""
		If the node list is empty or more nodes than are available
		were requested, gethost returns -1

		Returns the execnet gateway on success, -1 otherwise.
		"""
		if src == "": return -1
		try: gate = self._getq.get(True)
		except Queue.Empty:
			logging.info("Checking threads...")
			execnettle.checkthreads(self)
			return -1
		try:
			return execnet.makegateway("ssh=ac-oslab@"+gate).remote_exec(src, **kwargs)
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

	def terminate(self):
		"""
		Terminate our host acquisition threads.
		"""
		logging.info("Setting farmer lock")
		self._xfarmer.set()
		logging.info("Setting butcher lock")
		self._xbutcher.set()
		self._farmer.join()
		self._butcher.join()

	def __str__(self):
		s = "Execnettle instance:\n"
		s += " Farmer: " + self._farmer.name + "\n"
		s += " Butcher: " + self._butcher.name + "\n"
		s += " getq size = " + str(self._getq.qsize()) + "\n"
		s += " remq size = " + str(self._remq.qsize()) + "\n"
		return s

	@staticmethod
	def startthread(self, src, daemon=False):
		"""
		A general function to start a thread with the provided source code (src).
		You may also set whether it is a daemon (True/False).

		Returns the thread.
		"""
		t = threading.Thread(target=src, args=(self,))
		t.daemon=daemon
		t.start()
		return t

	@staticmethod
	def checkthreads(self):
		"""
		Perform a heartbeat check on the farmer/butcher threads, which control host
		acquisition. If either are dead, then start the other.

		Returns nothing.
		"""
		if not self._farmer.is_alive():
			if self._xfarmer.is_set(): self._xfarmer.clear()
			self._farmer = startthread(harvestnodes)
		if not self._butcher.is_alive():
			if self._xbutcher.is_set(): self._xbutcher.clear()
			self._butcher = startthread(slaughternodes)

	@staticmethod
	def slaughternodes(self):
		"""
		Repeatedly remove from the top of the node removal queue.

		Returns nothing.
		"""
		while not self._xfarmer.is_set():
			try: rem = self._remq.get(True, 2)
			except Queue.Empty: continue # XXX
			if rem != None: rem.close()

	@staticmethod
	def harvestnodes(self):
		"""
		Continually scan the specified subnet for port 22 using nmap. Loop over the
		found hosts, looking for port 22 being open. If so, then
		"""
		nm = nmap.PortScanner()
		while not self._xbutcher.is_set():
			nm.scan(hosts='10.14.10.0/24', arguments='-p 22')
			for h in nm.all_hosts():
				if self._xbutcher.is_set(): break # XXX
				if nm[h]['tcp'][22]['state'] == 'open':
					try: self._getq.put(h, True, 1)
					except Queue.Full: continue # XXX
