"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: Hong Kai Koh
   Usercode: hkk18
"""


def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    
    listPts = [] #list to be returned
    data = open(filename).read().splitlines() #classic ol' file reading
    
    for i in range(N):
        x_val, y_val = data[i].split()
        x_val, y_val = float(x_val), float(y_val)
        listPts.append((x_val, y_val))    
    
    return listPts


def theta(pointA, pointB):
    """Computes an approximation of the angle between
          the line AB and a horizontal line through A.
          -From the lecture notes-
    """
    
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
        
    else:
        t = dy/(abs(dx) + abs(dy))

    if dx < 0:
        t = 2 - t
        
    elif dy < 0:
        t = 4 + t
        
    return t * 90


def get_min_index(listPts):
    """Gets and returns index of the entry 
          with the smallest y value.
    """
    
    min_index = 0 #initialize index of min y value
    min_x, min_y = listPts[min_index] #initialize first pair as placeholder for min pair
    index = 0 
    
    while index < len(listPts):
        curr_x, curr_y = listPts[index] #initalize current iterated values of x and y
        
        if curr_y < min_y: #if smaller than current min_y value
            min_y = curr_y 
            min_index = index
            
        elif curr_y == min_y: #if both y values are equal
            
            if curr_x > min_x: #chose rightmost point
                min_index = index
                
        index += 1
        
    return min_index


def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of m tuples
          [(u0,v0), (u1,v1), ...]    
    """
    
    chull = [] #intialize list of tuples for convex hull
    input_list = []
    i = 0
    v = 0
    pk = get_min_index(listPts) #index of point with min y value
    
    for pts in listPts:
        input_list.append(pts) #list of all points
        
    input_list.append(listPts[pk])
    lenth = len(input_list) - 1
    
    #while (i == 0) or (min index != length of total list - duplicate entry of min point and min y value != y value of last entry in list)
    while i == 0 or (pk != lenth and input_list[pk][1] != input_list[lenth][1]):
        chull.append(input_list[pk])
        input_list[i], input_list[pk] = input_list[pk], input_list[i] #swap
        minAngle = 361
        
        for j in range(i+1, len(input_list)):
            angle = theta(input_list[i], input_list[j]) #find angle between line and pi
            
            if angle < minAngle and angle > v and input_list[j] != input_list[i]:
                minAngle = angle
                pk = j
                
        i += 1
        v = minAngle

    #if not at end of list and same y values
    if pk != lenth and input_list[pk][1] == input_list[lenth][1]:
        chull.append(input_list[pk])
    
    return chull


def lineFn(ptA, ptB, ptC):
    """Find directed line.
          -From notes-
    """
    
    return (ptB[0]-ptA[0]) * (ptC[1]-ptA[1]) - \
           (ptB[1]-ptA[1]) * (ptC[0]-ptA[0])

def isCCW(ptA, ptB, ptC):
    """Checks if is counter-clockwise direction.
          -From notes-
    """
    
    return lineFn(ptA, ptB, ptC) > 0


def simple_closed_path(listPts):
    """Find simple closed path to obtain sequential
          ordering of the list of input points
          such that p0 has the minimum y-coord.
    """
    
    p0 = get_min_index(listPts) #rightmost lowest point
    
    sorted_list = sorted(listPts, key=lambda pair: theta(listPts[p0],pair)) #sort according to angle of coord pair
    
    p0 = get_min_index(sorted_list) #set new p0 value    
    
    return (sorted_list, p0)


def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of m tuples
         [(u0,v0), (u1,v1), ...]  
    """
    
    chull = [] #intialize list of tuples for convex hull
    
    sorted_list, p0 = simple_closed_path(listPts)
    
    chull = [sorted_list[p0], sorted_list[1], sorted_list[2]] #use list instead of the actual stack as python's list methods of append and pop works like an actual stack and is more convenient as there is no need to import anything.
    
    for i in range(3, len(sorted_list)): #process each point in list
        
        while not (isCCW(chull[-2], chull[-1], sorted_list[i])):
            chull.pop()
            
        chull.append(sorted_list[i])
    
    return chull


def process_chull(listPts, order=0):
    """Process and sorts parts of the convex hull.
          To be used in Andrew's Monotone Chain Algorithm.
          Order set as 0 by default to process in normal order
          of listPts. If order is not 0, function will process
          in reversed order of listPts.
    """
    
    chull = [] #initialize list 
    
    if order != 0: #reverse order for listPts
        listPts.reverse()
        
    for coord in listPts:
        
        while len(chull) >= 2 and \
              lineFn(chull[-2], chull[-1], coord) <= 0:
            chull.pop()
    
        chull.append(coord)    
    
    return chull    
    
    
def amethod(listPts):
    """Returns the convex hull vertices computed using 
          a third algorithm.
          -Andrew's Monotone Chain Algorithm-
    """
    
    chull = [] #intialize list of tuples for convex hull  
    listPts1 = sorted(set(listPts)) #sorts list and removes any duplicate coord pair
    
    if len(listPts) < 2: #if only at most 1 unique coord pair
        chull = listPts
        
    else:
        lower = process_chull(listPts1) #normal order for listPts
        upper = process_chull(listPts1, 1) #reverse the order of listPts
        chull = lower[1:] + upper[1:] #add the parts together and remove duplicate entries in each part
        
    return chull


def main():
    
    listPts = readDataPts('B_30000.dat', 30000)  #change for other testfiles
    
    giftwrap_list = giftwrap(listPts)
    graham_list = grahamscan(listPts)
    monotone_list = amethod(listPts)
    
    print('Giftwrap returned: ')
    print(giftwrap_list)  
    print()
    print('Graham returned: ')
    print(graham_list)  
    print()
    print('Monotone returned: ')
    print(monotone_list)  
    print()
    
    #check if lists returned are the same for each algorithm
    check = 'Passed all checks' #ideal situation
    for item in (graham_list):
        
        if item not in giftwrap_list:
            check = 'Failed in Giftwrap and Graham'
            break      
        
        if item not in monotone_list:
            check = 'Failed in Monotone Chain and Graham'
            break
        
    print(check)   
 
 
if __name__  ==  "__main__":
    main()