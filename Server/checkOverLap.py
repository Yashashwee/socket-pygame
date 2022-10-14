def checkOverlap(player, danner):
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
