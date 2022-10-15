import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
import socketio
import unittest
import time
import os
sio = socketio.Client()


class test_serverEvents(unittest.TestCase):
    """ server events testing class"""
    def test_events(self):
        """testing server events"""
        #sio.emit("input", sio.sid, callback=checkReturn)
        with open("testOP.txt", "r") as f1, open("sample.txt", "r") as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            self.assertEqual(len(lines1), len(lines2), "Success size")
            for count, line1, line2 in zip(range(len(lines1)), lines1, lines2):
                msg = "line "+str(count)
                line2 = line2.strip()
                line1 = line1.strip()
                self.assertEqual(line1, line2, msg)


def checkReturn(*args):

    if len(args) > 0:
        with open("testOP.txt", "a+") as f:
            for i in range(len(args)):
                writeStr = str(args[i])+"\n"
                f.write(writeStr)


if __name__ == "__main__":
    sio.connect('http://0.0.0.0:5004')
    # sio.connect("https://socket-game-project.herokuapp.com/")

    # Testing all server events
    sio.emit("message", "Hello", callback=checkReturn)
    time.sleep(1)
    sio.emit("message", "NewMessage", callback=checkReturn)
    time.sleep(1)
    sio.emit("user", {"name": "Dummy", "choice": 0}, callback=checkReturn)
    time.sleep(1)
    sio.emit("user", {"name": "Dummy2", "choice": 3}, callback=checkReturn)
    time.sleep(1)
    sio.emit("nextkey", {"Player": [
        130, 130], "Danner": None, "frameNo": 404, "winner": None}, callback=checkReturn)
    time.sleep(1)
    sio.emit("nextkey", {"Player": None, "Danner": [
             140, 140], "frameNo": 404, "winner": None}, callback=checkReturn)
    time.sleep(1)
    sio.emit("resetPlayers", callback=checkReturn)
    time.sleep(1)
    sio.emit("user", {"name": "Dummy", "choice": 0}, callback=checkReturn)
    time.sleep(1)
    sio.emit("user", {"name": "Dummy2", "choice": 3}, callback=checkReturn)
    time.sleep(1)
    sio.emit("nextkey", {"Player": [
        803, 130], "Danner": None, "frameNo": 404, "winner": None}, callback=checkReturn)
    time.sleep(1)

    # Compare with sample outputs
    var = unittest.TestLoader().loadTestsFromTestCase(test_serverEvents)
    unittest.TextTestRunner(verbosity=2).run(var)

    sio.disconnect()
    # remove generated output
    os.remove("testOP.txt")
