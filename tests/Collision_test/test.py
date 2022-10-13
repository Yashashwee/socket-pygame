import os
import sys
import unittest

from collision import *

# unit test
class test_parser(unittest.TestCase):

	# checking if the player collision is done correctly
	def test_player2player_collision(self):
		self.assertEqual(checkOverlap([100,100],[100,110]),True)
		self.assertEqual(checkOverlap([100,100],[90,100]),True)
		self.assertEqual(checkOverlap([100,100],[100,90]),True)
		self.assertEqual(checkOverlap([100,100],[110,100]),True)
		self.assertEqual(checkOverlap([100,100],[110,110]),True)
		self.assertEqual(checkOverlap([100,100],[90,110]),True)
		self.assertEqual(checkOverlap([100,100],[90,90]),True)
		self.assertEqual(checkOverlap([100,100],[110,90]),True)

		self.assertNotEqual(checkOverlap([100,100],[80,100]),True)
		self.assertNotEqual(checkOverlap([100,100],[100,80]),True)
		self.assertNotEqual(checkOverlap([100,100],[120,100]),True)
		self.assertNotEqual(checkOverlap([100,100],[100,120]),True)

# added this condition so that this only runs if this file is run directly and not imported 
if __name__ == "__main__":
	var=unittest.TestLoader().loadTestsFromTestCase(test_parser)
	unittest.TextTestRunner(verbosity=2).run(var)

	
