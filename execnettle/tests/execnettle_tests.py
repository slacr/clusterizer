import unittest, sys
sys.path.append('../')
from execnettle.execnettles import *

class ExecnettleTests(unittest.TestCase):
	def setUp(self):
		

# 	def watwegot(self):
# 		print("***********watwegot**************")
# 		print("we've gota farmer named "+ self._farmer.name)
# 		print("and a butcher named "+self._butcher.name)
# 		print("a getq of size " +str(self._getq.qsize()))
# 		print("a remq of size "+str(self._remq.qsize()))
# 		print("***********watwegot**************")
# 
# 	def multiplier(channel, factor):
# 		while not channel.isclosed():
# 			param = channel.receive()
# 			channel.send(param * factor)
# 
# if __name__ == "__main__":
# 		print("Testing execnettles.py...")
# 		unittest.main()
# 
"""
Test material to cludge:


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
	t.terminate()
"""
