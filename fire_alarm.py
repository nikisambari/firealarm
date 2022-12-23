import cv2
import threading
import smtplib
import playsound
import tkinter as tk


fire_cascade=cv2.CascadeClassifier("fire_detection.xml")



def send_mail_function():
    email = smtplib.SMTP('smtp.gmail.com', 587)
    email.starttls()
    email.login("nikitasambari@gmail.com", "")
    message = "FIRE ALERT!!!!!!"
    email.sendmail("nikitasambari@gmail.com", "sambarinikita@gmail.com", message)
    print("DONE")
    email.quit()
    # add after gui

def sys(cap):
     runonce = False
     while True:
         success, img = cap.read()
         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         fire = fire_cascade.detectMultiScale(gray, 1.2, 5)



         for (x, y, w, h) in fire:
             cv2.rectangle(img, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
             if w > 120 and h>120:
                 cv2.putText(img, "high intensity", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
             elif w<100 and h< 100:
                  cv2.putText(img, "low intensity", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
             else:
                 cv2.putText(img, "small flame", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0),2)

             threading.Thread(target=play_alarm_sound_function).start()
             if runonce == False:
                print("Mail send initiated")
                threading.Thread(target=send_mail_function).start()  # To call alarm thread
                runonce = True
             if runonce == True:
                print("Mail is already sent once")
                runonce = True

         cv2.imshow("FIRE DETECTOR", img)

         if cv2.waitKey(1) & 0xff == ord("q"):
             break;

def play_alarm_sound_function():
        playsound.playsound('alarm_beeps.mp3',True)
def main():

    framew = 680
    frameh = 420
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, framew)
    cap.set(4, frameh)
    but = True
    runonce = False
    sys(cap)

main()
