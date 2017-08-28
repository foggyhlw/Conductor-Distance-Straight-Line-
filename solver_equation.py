import numpy as np
#
dec=4
#code found at:
#http://stackoverflow.com/questions/2824478/shortest-distance-between-two-line-segments
def closestDistanceBetweenLines(a0,a1,b0,b1,clampAll=False,clampA0=False,clampA1=False,clampB0=False,clampB1=False):

    ''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
        Return the closest points on each segment and their distance
    '''

    # If clampAll=True, set all clamps to True
    if clampAll:
        clampA0=True
        clampA1=True
        clampB0=True
        clampB1=True


    # Calculate denomitator
    A = a1 - a0
    B = b1 - b0
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)

    _A = A / magA
    _B = B / magB

    cross = np.cross(_A, _B);
    denom = np.linalg.norm(cross)**2


    # If lines are parallel (denom=0) test if lines overlap.
    # If they don't overlap then there is a closest point solution.
    # If they do overlap, there are infinite closest positions, but there is a closest distance
    if not denom:
        d0 = np.dot(_A,(b0-a0))

        # Overlap only possible with clamping
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A,(b1-a0))

            # Is segment B before A?
            if d0 <= 0 >= d1:
                if clampA0 and clampB1:
                    if np.absolute(d0) < np.absolute(d1):
                        return a0,b0,np.linalg.norm(a0-b0)
                    return a0,b1,np.linalg.norm(a0-b1)


            # Is segment B after A?
            elif d0 >= magA <= d1:
                if clampA1 and clampB0:
                    if np.absolute(d0) < np.absolute(d1):
                        return a1,b0,np.linalg.norm(a1-b0)
                    return a1,b1,np.linalg.norm(a1-b1)


        # Segments overlap, return distance between parallel segments
        return None,None,np.linalg.norm(((d0*_A)+a0)-b0)



    # Lines criss-cross: Calculate the projected closest points
    t = (b0 - a0);
    detA = np.linalg.det([t, _B, cross])
    detB = np.linalg.det([t, _A, cross])

    t0 = detA/denom;
    t1 = detB/denom;

    pA = a0 + (_A * t0) # Projected closest point on segment A
    pB = b0 + (_B * t1) # Projected closest point on segment B


    # Clamp projections
    if clampA0 or clampA1 or clampB0 or clampB1:
        if clampA0 and t0 < 0:
            pA = a0
        elif clampA1 and t0 > magA:
            pA = a1

        if clampB0 and t1 < 0:
            pB = b0
        elif clampB1 and t1 > magB:
            pB = b1

        # Clamp projection A
        if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
            dot = np.dot(_B,(pA-b0))
            if clampB0 and dot < 0:
                dot = 0
            elif clampB1 and dot > magB:
                dot = magB
            pB = b0 + (_B * dot)

        # Clamp projection B
        if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
            dot = np.dot(_A,(pB-a0))
            if clampA0 and dot < 0:
                dot = 0
            elif clampA1 and dot > magA:
                dot = magA
            pA = a0 + (_A * dot)

#return points and distance
    return round(np.linalg.norm(pA-pB),dec),pB,pA
#return distance
    # return np.linalg.norm(pA-pB)
##
##a0=np.array([12,2.4,25])
##a1=np.array([0,6.25,12])
##b0=np.array([12,2.9,21.5])
##b1=np.array([0,4.05,12])
##c0=np.array([12,2.4,18])
##c1=np.array([0,8.45,12])
##print('A-B:   '+str(closestDistanceBetweenLines(a0,a1,b0,b1))+'m')
##print('B-C:   '+str(closestDistanceBetweenLines(c0,c1,b0,b1))+'m')
##print('A-C:   '+str(closestDistanceBetweenLines(a0,a1,c0,c1))+'m')
##
##a0=np.array([22,2.4,25])
##a1=np.array([0,6.25,12])
##b0=np.array([22,2.9,21.5])
##b1=np.array([0,4.05,12])
##c0=np.array([22,2.4,18])
##c1=np.array([0,8.45,12])
##print('A-B:   '+str(closestDistanceBetweenLines(a0,a1,b0,b1))+'m')
##print('B-C:   '+str(closestDistanceBetweenLines(c0,c1,b0,b1))+'m')
##print('A-C:   '+str(closestDistanceBetweenLines(a0,a1,c0,c1))+'m')
##
##print('\n')
##a00=np.array([12,2.4,25])
##b11=np.array([0,6.25,12])
##b00=np.array([12,2.9,21.5])
##a11=np.array([0,4.05,12])
##c00=np.array([12,2.4,18])
##c11=np.array([0,8.45,12])
##print('A-B:   '+str(closestDistanceBetweenLines(a00,a11,b00,b11))+'m')
##print('B-C:   '+str(closestDistanceBetweenLines(c00,c11,b00,b11))+'m')
##print('A-C:   '+str(closestDistanceBetweenLines(a00,a11,c00,c11))+'m')
