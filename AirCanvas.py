'''
1. On running the code, a single window pops up. Position the tracker at the center of this window and left-click to detect the color of the tracker.
2. After finishing the previous step, The canvas pops up with the pointer as the default tool. Selecting any color (other than white) will change the tool to paintbrush.
'''

import cv2
import numpy as np

vid = cv2.VideoCapture(0) 
c = False
H = 90 #Default hue value, green
tool = "pointer" #default tool
coor = [] #Coordinates list
state_val = 1  
color = (0,0,0) #B
thickness = 2
paint = np.zeros((680,790,3)) + 255 #Creating a white painting window.

def painter(): #Painting window GUI
   cv2.rectangle(paint,(0,0), (790,680), (255,255,255), -1)
   cv2.rectangle(paint,(50,150), (690,630), (255,255,0), 2)
   cv2.rectangle(paint,(10,10), (780,670), (255,255,0), 2)
   
   cv2.rectangle(paint,(50,50), (130,130), (255,0,0), -1)  #b
   cv2.rectangle(paint,(190,50), (270,130), (0,255,0), -1) #g
   cv2.rectangle(paint,(330,50), (410,130), (0,0,255), -1) #r
   
   cv2.rectangle(paint,(50,50), (130,130), (0,0,0), 1)
   cv2.rectangle(paint,(190,50), (270,130), (0,0,0), 1)
   cv2.rectangle(paint,(330,50), (410,130), (0,0,0), 1)
   cv2.rectangle(paint,(470,50), (550,130), (0,0,0), -1)
   cv2.rectangle(paint,(610,50), (690,130), (0,0,0), 1)

   cv2.rectangle(paint,(720,250), (760,290), (0,0,0), 1)
   cv2.rectangle(paint,(730,260), (750,280), (0,0,0), 2)
   cv2.rectangle(paint,(720,310), (760,350), (0,0,0), 1)
   cv2.circle(paint,(740,330), 12, (0,0,0), 2)
   cv2.rectangle(paint,(720,370), (760,410), (0,0,0), 1)
   cv2.line(paint,(730,380), (750,400), (0,0,0), 2)
   cv2.rectangle(paint,(720,430), (760,470), (0,0,0), 1)
   cv2.circle(paint,(740,450), 2, (0,0,0), 2)
painter()


def tracker(event, x, y, flags, param): #Fuction to switch tracking colors
   global c, H
   if event == cv2.EVENT_RBUTTONUP and c==1:
      c=False
      color = (255,255,255)
   if event == cv2.EVENT_LBUTTONUP and c==0:
      H= hsv[240,320][0]
      c=True
      
def mouse(event, x, y, flags, param): #Mouse controls for painting window
      global tool,init,color, thickness
      if event == cv2.EVENT_LBUTTONUP and 50<y<130:
          tool = "draw"
          if 50<x<130:
              color = (255,0,0)
          if 190<x<270:
              color = (0,255,0)
          if 330<x<410:
              color = (0,0,255)
          if 470<x<550:
              color = (0,0,0)
          if 610<x<690:
              paint = np.zeros((680,740,3)) + 255
              painter()
              tool = "pointer"
      if event == cv2.EVENT_LBUTTONDOWN and 720<x<760:
         init = 1
         if 250<y<290:
            tool = "sq"
         if 310<y<350:
            tool = "cr"
         if 370<y<410:
            tool = "ln"    
      if event == cv2.EVENT_LBUTTONUP and 720<x<760:
         init = 0
         if 430<y<470:
            if tool == "draw":
               tool = "pointer"
            else:
               tool = "draw"           

              
while 1:
    
    cam = vid.read(0)[1] #Reading camera footage as frames
    cam = cv2.flip(cam,1) #Flipping the camera to get a non-inverted frame
    hsv = cv2.cvtColor(cam, cv2.COLOR_BGR2HSV) #BGR to HSV
    lower = np.array([H-10,100,100]) 
    upper = np.array([H+10,255,255])
    mask = cv2.inRange(hsv, lower, upper) 
    kernel = np.ones((7,7),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) #Removing noice
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) 
    
    if c == True:
        cv2.imshow('cam',cam)
        M = cv2.moments(mask) #Findind COM for coordinates of tracker
        if M["m00"] != 0 and len(mask)>0:
            cX = int(M["m10"] / M["m00"])+50
            cY = int(M["m01"] / M["m00"])+150
            if cX<= 690 and cY<=630: #Checking to see if the coordinates are within painting window
                draw = cv2.circle(cam, (cX-50, cY-150), 5,color, -1)
                cv2.imshow('cam',draw)
                cv2.setMouseCallback("cam", tracker)
                
                if tool =="draw": #Paintbrush
                    paint = cv2.line(paint, (cXo, cYo), (cX,cY),color,thickness)
                    state = paint.copy()
                    
                if tool == "sq": #Rectangular tool
                    if init ==1:
                       if state_val == 1:
                           state = paint.copy()
                           state_val = 0
                       paint = state.copy()
                       coor.append(cX)
                       coor.append(cY)
                       paint = cv2.rectangle(paint, (cXo, cYo), (coor[0],coor[1]),color,thickness)
                    if init == 0:
                       paint = cv2.rectangle(state, (cXo,cYo),(coor[0],coor[1]),color,thickness)
                       state_val = 1
                       coor.clear()
                       tool = "pointer"
                       
                if tool == "pointer": #Pointer, marks the pointer on the screen
                   state = paint.copy()
                   
                   paint = cv2.circle(paint,(cX,cY),1,color,thickness)
                
                if tool == "cr": #Circle tool
                    if init ==1:
                       if state_val == 1:
                           state = paint.copy()
                           state_val = 0
                       paint = state.copy()
                       coor.append(cX)
                       coor.append(cY)
                       dist = int((((cX - coor[0])**2 + (cY - coor[1])**2)**0.5)/2)
                       a = int((coor[0]+ cX)/2)
                       b = int((coor[1]+ cY)/2)
                       paint = cv2.circle(paint, (a,b),dist,color,thickness)
                    if init == 0:
                      dist = int((((cX - coor[0])**2 + (cY - coor[1])**2)**0.5)/2)
                      a = int((coor[0]+ cX)/2)
                      b = int((coor[1]+ cY)/2)
                      paint = cv2.circle(state, (a,b),dist,color,thickness)
                      state_val = 1
                      coor.clear()
                      tool = "pointer"
                      
                if tool == "ln": #Line tool
                    if init ==1:
                       if state_val == 1:
                           state = paint.copy()
                           state_val = 0
                       paint = state.copy()
                       coor.append(cX)
                       coor.append(cY)
                       paint = cv2.line(paint, (coor[0],coor[1]), (cX,cY),color,thickness)
                    if init == 0:
                      dist = int((((cX - coor[0])**2 + (cY - coor[1])**2)**0.5)/2)
                      paint = cv2.line(state, (coor[0],coor[1]),(cX,cY),color,thickness)
                      state_val = 1
                      coor.clear()
                      tool = "pointer"
                      
                cv2.imshow('paint',paint)
                cv2.setMouseCallback("paint", mouse)
                cXo = cX
                cYo = cY
                
                if tool == "pointer": #Removes pointer on the screen
                   paint = state.copy() 
            
    else: #If c is False
        draw = cv2.circle(cam, (320,240), 20, (0,255,0), 2)
        cv2.imshow('cam',draw)
        cv2.setMouseCallback("cam", tracker)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      
vid.release()
cv2.destroyAllWindows()

    

    
