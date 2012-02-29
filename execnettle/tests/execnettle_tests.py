"""
Test specs for execnettles.py
"""

import unittest, sys

sys.path.append('../')
from execnettle.execnettles import *

class ExecnettleTests(unittest.TestCase):
	def setUp(self):
		self.en = Execnettle() # def constructor		
		self.en1 = Execnettle(0) # edge 1
		self.en2 = Execnettle(sys.maxint) # edge 2
		self.en3 = Execnettle(-3) # edge 3
		self.en4 = Execnettle("wat") # edge 4

	def test_str_conversion(self):
		str(self.en)
		self.en.terminate()
	
	def test_inline(self):
		p = self.en.gethost("channel.send(channel.receive()+1)")
		p.send(1)
		self.assertEqual(p.receive(), 2)
		print(self.en)
		self.en.terminate()
	
	def test_funcs(self):
		p = []
		for i in range(2): #lol
			p.append(self.en.gethost(multiplier, factor=4))
			p[i].send(i)
			print("got factor: "+str(p[i].receive()))
		print(self.en)
		for i in range(2): self.en.killhost(p[i])
		print(self.en)
		self.en.terminate()

	def test_modules(self):
		sys.path.append('tests/')
		import remote1
		p = self.en.gethost(remote1)
		print(p.receive())
		self.en.terminate()

# Helper funcs
def multiplier(channel, factor):
	while not channel.isclosed():
		param = channel.receive()
		channel.send(param * factor)

if __name__ == "__main__":
	print("Testing execnettles.py...")
	suite = unittest.TestLoader().loadTestsFromTestCase(ExecnettleTests)
	unittest.TextTestRunner(verbosity=2).run(suite)
