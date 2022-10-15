def distance(x1, y1, x2, y2):
    return math.sqrt((y1-y2)**2 + (x1-x2)**2)


def predict_player_pos(pos1, pos2, val):
    """ Basically the objective of player is to
        maximize its distance from danner and 
        minimize its distance from winning position
        that has been implemented
        """
    if(val == 0):  # its a player
        points = []
        x = pos1[0]
        y = pos1[1]
        points.append([x-7, y+7])
        points.append([x, y+7])
        points.append([x+7, y+7])
        points.append([x+7, y])
        points.append([x+7, y-7])
        points.append([x, y-7])
        points.append([x-7, y-7])
        points.append([x-7, y])

        # print("POINTS = ",points)

        dist_p2 = []

        for i in range(8):
            dist_p2.append(
                distance(points[i][0], points[i][1], pos2[0], pos2[1]))

        dist_win = []
        for i in range(8):
            dist_win.append(distance(points[i][0], points[i][1], 802, 295))

        dist = []
        for i in range(8):
            dist.append(dist_p2[i]/dist_win[i])

        max1 = dist[0]
        maxpos = 0

        for i in range(1, 8):
            if(dist[i] > max1):
                max1 = dist[i]
                maxpos = i

        return([points[maxpos][0], points[maxpos][1]])

    else:  # its a danner
        points = []
        x = pos1[0]
        y = pos1[1]
        points.append([x-7, y+7])
        points.append([x, y+7])
        points.append([x+7, y+7])
        points.append([x+7, y])
        points.append([x+7, y-7])
        points.append([x, y-7])
        points.append([x-7, y-7])
        points.append([x-7, y])

        dist = []

        for i in range(8):
            dist.append(distance(points[i][0], points[i][1], pos2[0], pos2[1]))

        min1 = dist[0]
        minpos = 0

        for i in range(1, 8):
            if(dist[i] < min1):
                min1 = dist[i]
                minpos = i

        return([points[minpos][0], points[minpos][1]])
