import cv2
import pickle
import numpy as np
cap=cv2.VideoCapture("http://192.168.1.16:4747/video")
with open("cparkyt",'rb')as f:
     points=pickle.load(f)


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)
client = gspread.authorize(cerds)
sheet = client.open("carparking").worksheet('sheet1') # เป็นการเปิดไปยังหน้าชีตนั้นๆ
# cell=sheet.cell(car,2).value
# pprint(cell)
sheet.update_cell(2,2,1)
# cell=sheet.cell(car,2).value




def crop(f):
    scount=0
    for pts in points:
        
        x,y=pts
        crop=f[y:y+h,x:x+w]
#        cv2.imshow(str(x*y),crop)
        count=cv2.countNonZero(crop)
        if count < 150:
           color = (0,255,0)
           cv2.putText(frame,str(count),(x,y -1),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
           cv2.rectangle(frame,pts,(pts[0]+w,pts[1]+h),(0,255,0),2)
           scount+=1
        else:
            color = (0,0,255)
            cv2.putText(frame,str(count),(x,y -1),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
            cv2.rectangle(frame,pts,(pts[0]+w,pts[1]+h),(0,0,255),2)
        c = "F"
        n = 0
        while c == "F":
            if pts == points[n]:
                c = "T"
                if color == (0,255,0):
                    # print('p : ' + str(n)  + ' ว่าง')
                    status = "ว่าง" 
                    colorline = "green"
                else:
                    # print('p : ' + str(n)  + 'ไม่ว่าง' )
                    status = "ไม่ว่าง"
                    colorline = "red"
                car = n + 2
                
                # pprint(cell)
               
            else:
                n = n + 1
        sheet.update_cell(2,3,status)
            
    cv2.putText(frame,f'FreeSpace:{scount}/{len(points)}',(20,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)        
       
                       
        
            


            
        
    

w,h=29,27

while True:
    success, frame = cap.read()
    if success==False:
        break

    frame=cv2.resize(frame,(640,480))
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frameBlur=cv2.GaussianBlur(gray,(5,5),1)
    frameThreshold=cv2.adaptiveThreshold(frameBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,105,9)
    frameMedian=cv2.medianBlur(frameThreshold,5)
    kernel=np.ones((3,3),np.uint8)
    FrameDilate=cv2.dilate(frameMedian,kernel,iterations=1)
    
    
   
    crop(FrameDilate)
    cv2.imshow("Frame",frame)
    

    
    
  
    
 
   
    
     
    if cv2.waitKey(32) & 0xFF == 27:
        break
cv2.destroyAllWindows()