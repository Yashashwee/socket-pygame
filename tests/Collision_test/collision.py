import math

def checkOverlap(player, danner):
	"""Get player 1 postion and its center of mass .
	Get player 2 postion and its cemter of mass
	. Check collision using the distance logic
	"""
	l1 = player
	r1 = [l1[0]+15, l1[1]-15]
	l2 = danner
	r2 = [l2[0]+15, l2[1]-15]

	# If one rectangle is on left side of other
	if l1[0] > r2[0] or l2[0] > r1[0]:
		return False

	# If one rectangle is above other
	if r1[1] > l2[1] or r2[1] > l1[1]:
		return False

	return True

# p1=[]
# p2=[]

# p1.append(int(input("Enter x coordinate of p1")))
# p1.append(int(input("Enter y coordinate of p1")))
# p2.append(int(input("Enter x coordinate of p2")))
# p2.append(int(input("Enter y coordinate of p2")))

# if(checkOverlap(p1,p2)):
# 	print("Collision happened")
# else:
# 	print("No collision")
