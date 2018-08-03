"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: Hong Kai Koh
   Usercode: hkk18
"""


import convexhull #make sure convexhull.py and convexhull_time.py are in the same folder
from time import time


def main():
    """Add-on time tracker for Convex Hull Algorithms
          of Giftwrap, Graham Scan and 
          Andrew's Monotone Chain Algorithm
    """
    
    listPts = convexhull.readDataPts('B_30000.dat', 30000) #change to whichever needed 
   
    #Gift Wrap Timer
    start_timer = time()
    giftwrap_list = convexhull.giftwrap(listPts)    
    print("Gift Wrap algorithm used {:.15f} seconds.".format(time() - start_timer))   
   
    #Graham Scan Timer
    start_timer = time()
    graham_list = convexhull.grahamscan(listPts)
    print("Graham Scan algorithm used {:.15f} seconds.".format(time() - start_timer))  
    
    #Monotone Chain Timer
    start_timer = time()    
    monotone_list = convexhull.amethod(listPts)     
    print("Monotone Chain algorithm used {:.15f} seconds.".format(time() - start_timer))  
    

if __name__  ==  "__main__":
    main()