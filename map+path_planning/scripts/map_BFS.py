#!/usr/bin/env python3

# import the required libraries:
import rospy
import numpy as np 
import cv2 #import openCV to python
########################Global variables######################
global maze_height
global maze_xidth  
global maze #two dimentional array of the map#

##############################################################
#function descriptions:
# inputs:maze path in the computer
# outputs :two dimntional array of the map with the 0 is the area of obstcles
# and 255 is available space the robot can go throw  
# #
def import_map (path):
 global maze_height
 global maze_xidth  
 global maze 

 # Save image in set directory 
 #note the map genrated from ARVIZ is .pgm  
 img = cv2.imread(path)  #Read maze 
 grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convert RGB image to grayscale
 ret, bw_img = cv2.threshold(grayImage,0,255,cv2.THRESH_BINARY) #Convert grayscale image to binary
 print(("array type:"),type(bw_img))
 bw_img = bw_img.astype(np.uint8)
 maze=bw_img
 cv2.imshow("Window", bw_img)

 maze_height, maze_xidth= bw_img.shape #get image dimenssions
######################################################################
#function descriptions:this function applys the BFS algorith and store the output points in queue
# inputs: map array ,start point , goal point ,direction of searsh cw or ccw
# outputs: the optimal path 
# #
def BFS(Map,Start,Goal,Direction):  # Direction for CCW -1  for CW 1

    Flag = False # Flag indicating if goal node is found
    
    # Initializing a queue 
    queue = []
    queue.append(Start)

    # Visited Nodes
    Visited = []

    # Parent Node Mapping
    Parents = np.zeros([384,384,2],dtype = int)


    while queue:   # If queue is not empty 

        Node = queue.pop(0)  # Pop first element in the queue

        if Node==Goal:   # Did we reach the goal?
            Flag = True
            break

        Neighbours = get_Neighbours(Node,Direction) # Get neighbours of this node

        for N in Neighbours: # For each neighbour of this node
            if not N in Visited and Map[N[0],N[1]]!=0:   # if this neighbour wasnt visited before and doesnt equal 0 (ie not an obstacle)
                queue.append(N)      # add to the queue
                Visited.append(N)     # add it to the visited
                Parents[N[0],N[1]] = Node  # add its parent node 

    if Flag == False:
        print('Mafesh path :(')

    if Flag == True:
        path = get_Path(Parents,Goal,Start) # this function returns the path to the goal 
        return path
    

#########################################################################
#function descriptions: this function get the optimal path that reached the goal in the queue
# inputs:the array of parents and the goal point and start point
# outputs:the BFS path  
# #
def get_Path(Parents,Goal,Start):

    path = []
    Node = Goal  # start backward 
    path.append(Goal)
   
    while not np.array_equal(Node, Start):

       path.append(Parents[Node[0],Node[1]])  # add the parent node 
       Node = Parents[Node[0],Node[1]]        # search for the parent of that node 
     
    path.reverse()
    return path


#########################################################################
#function descriptions:this function gets the 8 neighboors of the point 
# inputs: pint (x,y) , direction of searchb (1 cw),(-1 ccw)
# outputs: array of 8 points (x,y)  
# #
def get_Neighbours(Node,Direction):    # Returns neighbours of the parent node   Direction = 1 for Clockwise/ Direction = -1 for CCW 

    Neighbours = []
    
    if Direction==1:
        Neighbours.append([Node[0],Node[1]+1])
        Neighbours.append([Node[0]+1,Node[1]+1])
        Neighbours.append([Node[0]+1,Node[1]])
        Neighbours.append([Node[0]+1,Node[1]-1])
        Neighbours.append([Node[0],Node[1]-1])
        Neighbours.append([Node[0]-1,Node[1]-1])
        Neighbours.append([Node[0]-1,Node[1]])
        Neighbours.append([Node[0]-1,Node[1]+1])
                        
    if Direction==-1:
        Neighbours.append([Node[0],Node[1]+1])
        Neighbours.append([Node[0]-1,Node[1]+1])
        Neighbours.append([Node[0]-1,Node[1]])
        Neighbours.append([Node[0]-1,Node[1]-1])
        Neighbours.append([Node[0],Node[1]-1])
        Neighbours.append([Node[0]+1,Node[1]-1])
        Neighbours.append([Node[0]+1,Node[1]])
        Neighbours.append([Node[0]+1,Node[1]+1])

    return Neighbours

if __name__ == '__main__':     # Main function that is executed 
 import_map ('/home/youssef/map.pgm')
 #point (0,0) is the center of image so we need to move the coordinate to the center of the image
 # which is (192,192) then the point (1,1) is (191,193) and the point (2,3) is (190,195)#
 path = BFS(maze,[191,193],[190,195],1) 
 print("the path is:",path)
 print('height:', maze_height)
 print('width:', maze_xidth)
 print(maze)

 cv2.waitKey(0) #Maintain output window until user presses a key 
 cv2.destroyAllWindows() #Destroying present windows on screen
