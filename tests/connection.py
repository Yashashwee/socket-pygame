import os
import sys
import unittest
import time
import platform
if platform.system() == 'Linux':
    fileSystemGoBack='.'
else:
    fileSystemGoBack='..'

sys.path.insert(0, os.path.join(fileSystemGoBack,'Client'))
import client


class test_connection(unittest.TestCase):
	"""
	unit test class
	"""
	def test_connection1(self):
		"""
		checking if connection established or not
		"""
		client.sio.connect("https://socket-game-project.herokuapp.com/")
		self.assertEqual(client.temp,"I'm connected!","connection not established")
		client.sio.eio.disconnect(True)  

	def test_connection2(self):
		"""
		checking if exception raised in wrong connection (wrong url provided)
		"""
		with self.assertRaises(Exception):client.sio.connect("http://0.0.0.0:5004")

	def test_connection3(self):
		"""
		checking if exception raised in wrong connection (url not provided)
		"""
		with self.assertRaises(Exception):client.sio.connect("")
		
# added this condition so that this only runs if this file is run directly and not imported 
if __name__ == "__main__":
	var=unittest.TestLoader().loadTestsFromTestCase(test_connection)
	unittest.TextTestRunner(verbosity=2).run(var)
