import math

def checkOverlap(player1_pos, player2_pos):
	"""Get player 1 postion and its cemter of mass"""
	"""Get player 2 postion and its cemter of mass"""
	"""Check collision using the distance logic"""
	
	p1_x = player1_pos[0]
	p1_y = player1_pos[1]
	p2_x = player2_pos[0]
	p2_y = player2_pos[1]

	com_p1_x = p1_x + 7.5
	com_p1_y = p1_y + 7.5

	com_p2_x = p2_x + 7.5
	com_p2_y = p2_y + 7.5

	print("center of mass of p1 = ", com_p1_x, com_p1_y)
	print("center of mass of p2 = ", com_p2_x, com_p2_y)

	if(math.sqrt((com_p2_y-com_p1_y)**2 + (com_p2_x-com_p1_x)**2) <= 15):
		return True
	else:
		return False

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
