import os
import sys
import socketio
import time
import unittest

from collision import *

sio = socketio.Client()
# unit test


testArr = [
    [[100, 100], [100, 110]],
    [[100, 100], [90, 100]],
    [[100, 100], [100, 90]],
    [[100, 100], [110, 100]],
    [[100, 100], [110, 110]],
    [[100, 100], [90, 110]],
    [[100, 100], [90, 90]],
    [[100, 100], [110, 90]],
    [[100, 100], [80, 100]],
    [[100, 100], [100, 80]],
    [[100, 100], [120, 100]],
    [[100, 100], [100, 120]]
]


class test_collision(unittest.TestCase):

    # checking if the player collision is done correctly
    def test_player2player_collision(self):
        # self.assertEqual(checkOverlap([100, 100], [100, 110]), True)
        # self.assertEqual(checkOverlap([100, 100], [90, 100]), True)
        # self.assertEqual(checkOverlap([100, 100], [100, 90]), True)
        # self.assertEqual(checkOverlap([100, 100], [110, 100]), True)
        # self.assertEqual(checkOverlap([100, 100], [110, 110]), True)
        # self.assertEqual(checkOverlap([100, 100], [90, 110]), True)
        # self.assertEqual(checkOverlap([100, 100], [90, 90]), True)
        # self.assertEqual(checkOverlap([100, 100], [110, 90]), True)

        # self.assertNotEqual(checkOverlap([100, 100], [80, 100]), True)
        # self.assertNotEqual(checkOverlap([100, 100], [100, 80]), True)
        # self.assertNotEqual(checkOverlap([100, 100], [120, 100]), True)
        # self.assertNotEqual(checkOverlap([100, 100], [100, 120]), True)
        with open("testOP.txt", "r") as f1, open("sample.txt", "r") as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            for count, line1, line2 in zip(range(len(lines1)), lines1, lines2):
                line1 = line1.strip()
                line2 = line2.strip()
                self.assertEqual(line1, line2, count)


def checkReturn(*args):

    if len(args) > 0:
        with open("testOP.txt", "a+") as f:
            for i in range(len(args)):
                writeStr = str(args[i])+"\n"
                f.write(writeStr)


# added this condition so that this only runs if this file is run directly and not imported
if __name__ == "__main__":
    sio.connect('http://0.0.0.0:5004')
    # sio.connect("https://socket-game-project.herokuapp.com/")
    for coords in testArr:
        sio.emit("testoverlap", coords, callback=checkReturn)
        time.sleep(1)

    var = unittest.TestLoader().loadTestsFromTestCase(test_collision)
    unittest.TextTestRunner(verbosity=2).run(var)

    sio.disconnect()
    # remove generated output
    os.remove("testOP.txt")
