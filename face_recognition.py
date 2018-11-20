#!/usr/bin/python

import numpy as np
import time
import cv2
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

gmail_user = "***@gmail.com"
gmail_pwd = "***"

def SendMail(ImgFileName, count):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Reporte reconocimiento de rostros'
    msg['From'] = '***@gmail.com'
    msg['To'] = '***@gmail.com'

    text = MIMEText("Se ha detectado un diverso numero de personas en la estacion - No personas detectadas:  " + str(count))
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(gmail_user, gmail_pwd)
    s.sendmail(gmail_user, "***@gmail.com", msg.as_string())
    s.quit()





if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    count = 0

    while(True):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print "Rostros en imagen capturada " + str(len(faces))

        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        img_path = str(count) + '_image.jpg'
        cv2.imwrite(img_path, frame)

        count = count + 1 	
        cap.release()
        SendMail(img_path, len(faces))
        time.sleep(5)


    cv2.destroyAllWindows()
