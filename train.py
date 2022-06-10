import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import smtplib
from email.message import EmailMessage

window = tk.Tk()
#helv36 = tk.Font(family='Italic', size=36, weight='bold')
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
window.geometry('1280x720')
window.configure(background='#89cff0')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

imgycce = ImageTk.PhotoImage(Image.open("ycce.jpg"))
labelycce = tk.Label(window, image = imgycce)
labelycce.place(x=500,y=20)

#message = tk.Label(window, text="YCCE Attendence System" ,bg="#89cff0"  ,fg="white"  ,width=45  ,height=3,font=('times', 30, 'bold'))

#message.place(x=150, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="white"  ,bg="teal" ,font=('times', 15, ' bold ') )
lbl.place(x=350, y=200)


txt = tk.Entry(window,width=20  ,bg="white" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=650, y=215)


lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="white"  ,bg="teal"    ,height=2 ,font=('times', 15, ' bold '))
lbl2.place(x=350, y=275)

txt2 = tk.Entry(window,width=20  ,bg="white"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=650, y=290)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="white"  ,bg="teal"  ,height=2 ,font=('times', 15, ' bold underline '))
lbl3.place(x=350, y=375)

message = tk.Label(window, text="" ,bg="white"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
message.place(x=650, y=375)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="white"  ,bg="teal"  ,height=2 ,font=('times', 15, ' bold  underline'))
lbl3.place(x=350, y=450)


message2 = tk.Label(window, text="" ,fg="red"   ,bg="white",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold '))
message2.place(x=650, y=450)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
          import unicodedata
          unicodedata.numeric(s)
          return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>59:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('C:\Final_Year_Project\Face-Recognition-Based-Attendance-System-master\StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("C:\Final_Year_Project\Face-Recognition-Based-Attendance-System-master\TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("C:\Final_Year_Project\Face-Recognition-Based-Attendance-System-master\TrainingImageLabel\Trainner.yml")
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    df=pd.read_csv("C:\Final_Year_Project\Face-Recognition-Based-Attendance-System-master\StudentDetails\StudentDetails.csv")
    vid = cv2.VideoCapture(0)
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)
    while True:
        ret,frame=vid.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("C:\Final_Year_Project\Face-Recognition-Based-Attendance-System-master\ImagesUnknown"))+1
                cv2.imwrite("C:\Final_Year_Project\Face-Recognition-Based-Attendance-System-master\ImagesUnknown\Image"+str(noOfFile) + ".jpg", frame[y:y+h,x:x+w])            
            cv2.putText(frame,str(tt),(x,y+h),cv2.FONT_HERSHEY_COMPLEX, 1,(255,255,255),1)
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',frame) 
        if (cv2.waitKey(100)==ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    fileName="C:\Final_Year_Project\Face-Recognition-Based-Attendance-System-master\Attendance\Attendance"+date+"_"+".csv"
    #attendance.to_csv(fileName,index=False,mode='a')
    if(os.path.isfile(fileName)):
        attendance.to_csv(fileName, sep = '|', mode='a', index= False,header=False)
    else:
        attendance.to_csv(fileName, sep = '|', index= False)
    vid.release()
    cv2.destroyAllWindows()
    res=attendance
    message2.configure(text= res)

import smtplib
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email import encoders
from datetime import date


def emailsend():
    fromi="jakoick@gmail.com"
    to = "ojasthengadi21@gmail.com"
    message = MIMEMultipart()
    message['From'] = fromi
    message['To'] = to
    message['Subject'] ="Today's attendence"
    body_email = "Excel file attached"
    message.attach(MIMEText(body_email, 'plain'))
    today=date.today()
    d4 = today.strftime("%Y-%m-%d")
    file_name = "Attendance"+d4+"_"+".csv"
    attachment = open("C:\\Final_Year_Project\\Face-Recognition-Based-Attendance-System-master\\Attendance\\" + file_name,"rb")
    x = MIMEBase('application', 'octet-stream')
    x.set_payload((attachment).read())
    encoders.encode_base64(x)
    x.add_header('Content-Disposition', "attachment; file_name= %s" %file_name)
    message.attach(x)
    s_e = smtplib.SMTP('smtp.gmail.com', 587)
    s_e.starttls()
    s_e.login(fromi,"Ojas1234@")
    text = message.as_string()
    s_e.sendmail(fromi, to, text)
    res="Mail sent"
    message2.configure(text= res)
    s_e.quit()



# Details of the GUI present on screen 
clearButton = tk.Button(window, text="Clear", command=clear,fg="white"  ,bg="teal"  ,width=15  ,height=1 ,activebackground = "Green" ,font=('times', 15, ' bold '))
clearButton.place(x=900, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="white"  ,bg="teal"  ,width=15  ,height=1, activebackground = "Green" ,font=('times', 15, ' bold '))
clearButton2.place(x=900, y=280)
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=15  ,height=2, activebackground = "Green" ,font=('times', 15, ' bold '))
takeImg.place(x=350, y=550)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="white"  ,bg="orange"  ,width=15  ,height=2, activebackground = "Green" ,font=('times', 15, ' bold '))
trainImg.place(x=550, y=550)
trackImg = tk.Button(window, text="Attendence", command=TrackImages  ,fg="white"  ,bg="Green"  ,width=15  ,height=2, activebackground = "Green" ,font=('times', 15, ' bold '))
trackImg.place(x=750, y=550)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="red"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=950, y=550)
emailsend = tk.Button(window, text="Email", command=emailsend  ,fg="red"  ,bg="#25D366"  ,width=9  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
emailsend.place(x=650, y=620)

window.mainloop()
time.sleep(10)
