import os
import sys
import time
import platform
if platform.system() == 'Linux':
    fileSystemGoBack='.'
else:
    fileSystemGoBack='..'

# print(os.path.join(fileSystemGoBack,'Collision_test'))
sys.path.insert(0, os.path.join(fileSystemGoBack,'Collision_test'))
from collision import *


def conclusion(player,danner):
	if(checkOverlap(player,danner)):
		return ([False,True])

	else:
		if(player[0]>801):
			return([True,False])
		else:
			return([False,False])