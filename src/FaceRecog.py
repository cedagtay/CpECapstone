import cv2
import os
import sys

class FaceRecog():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    def __init__(self, haarcascade_data, data_path):
        self.face_classifier = cv2.CascadeClassifier(haarcascade_data)
        self.data_path = data_path
        
    def capture(self, name):
        count = 0
        dirname = self.data_path + "/" + name
        os.makedirs(dirname)
        while(True):
            ret, img = self.cam.read()
            img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray, 3, 1)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                cv2.imshow('image', img)
                cv2.imwrite(dirname+"/"+name+"." + str(count) + ".jpg", gray[y:y+h,x:x+w])
                count += 1

            key = cv2.waitKey(10) & 0xff
            if key == 27:
                break
            elif count == 3:
                break
            

        cv2.destroyAllWindows()
        return dirname
        
    def destroy(self):
        self.cam.release()
