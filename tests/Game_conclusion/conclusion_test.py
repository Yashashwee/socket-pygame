import os
import sys
import unittest

from game_conclusion import *

# unit test
class test_conclusion(unittest.TestCase):
	"""unit test class"""
	# checking if the player collision is done correctly
	def test_p1_win(self):
		""" player win logic testing """
		self.assertEqual(conclusion([802,250],[100,110]),[True,False])
		self.assertEqual(conclusion([802,265],[90,100]),[True,False])
		self.assertEqual(conclusion([802,278],[100,90]),[True,False])
		self.assertEqual(conclusion([802,332],[110,100]),[True,False])

		self.assertNotEqual(conclusion([521,432],[80,100]),[True,False])
		self.assertNotEqual(conclusion([624,523],[100,80]),[True,False])
		self.assertNotEqual(conclusion([500,278],[120,100]),[True,False])
		self.assertNotEqual(conclusion([800,184],[100,120]),[True,False])

	def test_p2_win(self):
		""" danner win logic testing """
		self.assertEqual(conclusion([100,100],[110,100]),[False,True])
		self.assertEqual(conclusion([201,184],[195,183]),[False,True])
		self.assertEqual(conclusion([100,320],[90,315]),[False,True])
		self.assertEqual(conclusion([332,100],[336,95]),[False,True])
		self.assertEqual(conclusion([100,100],[110,90]),[False,True])

		self.assertNotEqual(conclusion([521,432],[80,100]),[False,True])
		self.assertNotEqual(conclusion([624,523],[100,80]),[False,True])
		self.assertNotEqual(conclusion([802,278],[120,100]),[False,True])
		self.assertNotEqual(conclusion([800,184],[100,120]),[False,True])

	def test_none_win(self):
		""" none win logic testing """
		self.assertEqual(conclusion([200,100],[110,100]),[False,False])
		self.assertEqual(conclusion([232,100],[110,110]),[False,False])
		self.assertEqual(conclusion([542,100],[90,110]),[False,False])
		self.assertEqual(conclusion([224,100],[90,90]),[False,False])
		self.assertEqual(conclusion([671,100],[110,90]),[False,False])

		self.assertNotEqual(conclusion([100,100],[110,100]),[False,False])
		self.assertNotEqual(conclusion([210,220],[205,219]),[False,False])
		self.assertNotEqual(conclusion([802,278],[120,100]),[False,False])
		self.assertNotEqual(conclusion([802,324],[100,120]),[False,False])

# added this condition so that this only runs if this file is run directly and not imported 
if __name__ == "__main__":
	var=unittest.TestLoader().loadTestsFromTestCase(test_conclusion)
	unittest.TextTestRunner(verbosity=2).run(var)

	
