import sys
import os
import threading
import time
import urllib
import urllib2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

shit_score = -1

class Prioritizeratoration:

## we spawn the server and the timed check as threads.
	def init_prioritizeratoration(self):
#		self._check_clients = threading.Thread(target=Prioritizeratoration.check_client_relevance, args=(self,))
#		self._check_clients.start()

		self._metric_server = MetricHTTPServer(('', 8080), MetricServer)
		self._server_thread = self.startthread(self, Prioritizeratoration.run_metric_server)

		self._check_clients = self.startthread(self, Prioritizeratoration.check_client_relevance)

	def get_score(self, key):
		return self._metric_server.scores.get(key, shit_score)

## basically, clients that are alive should be reporting
## every minute. If they haven't reported in the last 
## minute then they get a shit score.
## i'm not sure how accurate our ntp settings are across
## labs though so for now i give them a 2 minute window

	@staticmethod
	def startthread(self, sauce, daemon=False):
		t = threading.Thread(target=sauce, args=(self,))
		t.daemon=daemon
		t.start()
		return t

	@staticmethod
	def check_client_relevance(self):
		while True:
			time.sleep(4)
			now = time.time()
			for key, value in self._metric_server.scores.items():
				if value[0] < now-9:
					self._metric_server.scores[key] = (now, shit_score)
					print "score should be shit for " + key

	@staticmethod
	def run_metric_server(self):
		try:
			for i in range(5):
				self._metric_server.handle_request()
				time.sleep(4)
		except KeyboardInterrupt:
			self._metric_server.socket.close()
	

class MetricClient:

	def __init__(self, port='8080', server='http://localhost'):
		self.port=port
		self.server=server
		self.post = threading.Thread(target=MetricClient.post, args=(self,))
		self.post.start()

	def loadavg(self):
		avg = 1
		return str(avg)

	def memusage(self):
		usg = 2
		return str(usg)

	def numcpus(self):
		cpus = 3
		return str(cpus)

	def numrams(self):
		rams = 4
		return str(rams)

	def post(self):
		while True:
			print "posting cli message"
			arg = {'time':str(time.time())}
			arg['loagavg'] = self.loadavg()
			arg['memusage'] = self.memusage()
			arg['numcpus'] = self.numcpus()
			arg['numrams'] = self.numrams()
			try: 
				time.sleep(4)
#				url = self.server+':'+self.port
				url = 'http://localhost:8080'
				data = urllib.urlencode(arg)
				req = urllib2.Request(url, data)
				response = urllib2.urlopen(req)
			except IOError:
				print "IOError happened!"
				break
		return None


class MetricHTTPServer(HTTPServer):
	def __init__( self, *args):
		super(MetricHTTPServer,self).__init__(*args)
		self.scores = {}

class MetricServer(BaseHTTPRequestHandler):

## keys are the src as seen by server; vales are {post_time, score}
## for now score is just the add of all fields sent in a given post

##  this will be where graphs and stuff are rendered....
	def do_GET(self):
		print "not what we hoped for"

	def do_POST(self):
		length = int(self.headers.getheader('content-length'))
		post_data = self.rfile.read(length)
		raw_data = urllib.unquote(post_data)
		
		print "received data: " + raw_data

		data = raw_data.split('&')
		for d in data:
			self.scores[client_address] = d.split('=')
			
		self.send_response(200)

if __name__=='__main__':
	print "initing prioritizeratoration"
	pri = Prioritizeratoration()
	pri.init_prioritizeratoration()
	print "initing client"
	cli = MetricClient(server='localhost')
	pri._server_thread.join()
	pri._check_clients.join()
	cli.post.join()
