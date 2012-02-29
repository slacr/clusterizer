import sys
import os
import threading
import time
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

shit_score = -1

class prioritizeratoration:
	def __init__(self):

## we spawn the server and the timed check as threads.
	def init_prioritizeratoration(self)
		self._metric_server = threading.thread(run_metric_server)
		self._metric_server.daemon = daemon
		self._metric_server.start()

		self._check_clients = threading.thread(check_client_relevance, self,)
		self._check_clients.daemon = daemon
		self._check_clients.start()

	def get_score(self, key):
		return self._metric_server.scores.get(key, shit_score)

## basically, clients that are alive should be reporting
## every minute. If they haven't reported in the last 
## minute then they get a shit score.
## i'm not sure how accurate our ntp settings are across
## labs though so for now i give them a 2 minute window
	@staticmethod
	def check_client_relevance(self):
		while True:
			time.sleep(60)
			now = time.time()
			for key, value in self._metric_server.scores.items():
				if value[0] < now-120:
					self._metric_server.scores[key] = shit_score

	@staticmethod
	def run_metric_server():
		try:
			server = HTTPServer(('127.0.0.1', 8080), QueueHttpServer)
			logger.info('Starting MetricServer')
			server.serve_forever()
		except KeyboardInterrupt:
			logger.info('^C received, shutting down server')
			server.socket.close()
	

class MetricClient:

	def __init__(self, port=8080, server=''):
		self.port=port
		self.server=server
		self.post = threading.thread(post, self,)
		self.post.daemon = daemon
		self.post.start()

	def loadavg():
		avg = 1
		return str(avg)

	def memusage():
		usg = 2
		return str(usg)

	def numcpus():
		cpus = 3
		return str(cpus)

	def numrams():
		rams = 4
		return str(rams)

	def post():
		while True:
			arg = {'time':str(time.time(), 'loagavg':loadavg(), 
							'memusage':memusage(), 'numcpus':numcpus(), 
							'numrams':numrams()}
			try: 
				u = urllib.urlopen(server+str(port), data=urllib.urlencode(arg)
				if 199 < u < 300:
					time.sleep(60)
			except IOError:
				break

class MetricServer(BaseHTTPRequestHandler):

## keys are the src as seen by server; vales are {post_time, score}
## for now score is just the add of all fields sent in a given post
	scores = {}

##  this will be where graphs and stuff are rendered....
	def do_GET(self):
		pass

	def do_POST(self):
		length = int(self.headers.getheader('content-length'))
		post_data = self.rfile.read(length)
		raw_data = urllib.unquote(post_data)
		
		print "received data: " + raw_data
