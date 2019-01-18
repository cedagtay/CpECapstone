import cv2
import numpy as np
from PIL import Image
import os
import sys

class FaceRecog():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def __init__(self, haarcascade_capture, haarcascade_recognize, trainer_file, data_path, database):
        self.face_classifier = cv2.CascadeClassifier(haarcascade_capture)
        self.face_trainer = cv2.CascadeClassifier(haarcascade_recognize)
        self.recognizer.read(trainer_file)
        self.data_path = data_path
        self.database = database
        self.trainer_file = trainer_file
        
    def capture(self, name, user_id):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        dirname = self.data_path + "/" + str(user_id)
        os.makedirs(dirname)
        count = 0

        while count <= 30:
            ret, img = cam.read()
            img = cv2.flip(img, 1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray, 3, 1)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                cv2.imshow('image', img)
                cv2.imwrite(dirname+"/"+name+"."+ str(count) + ".jpg", gray)
                count += 1
                
        cam.release()
        cv2.destroyAllWindows()

    def getImagesAndLabels(self, path):
        dictionary = {}
    
        for folder in os.listdir(path):
            fullPath = os.path.join(path,folder)
            dictionary[folder] = [os.path.join(fullPath, image) for image in os.listdir(fullPath)]
        
            faceSamples=[]
            ids = []
    
        for name,imagePaths in dictionary.items():
            PIL_imgs = [Image.open(imagePath) for imagePath in imagePaths] # convert it to grayscale
            imgs_numpy = [np.array(PIL_img,'uint8') for PIL_img in PIL_imgs]
                
            for img_numpy in imgs_numpy:
                faces = self.face_trainer.detectMultiScale(img_numpy)
                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(int(folder))
                        
        return faceSamples, ids

    def recognize(self, names):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        user_id = 0
        while True:
            ret, img_raw = cam.read()
            img = cv2.flip(img_raw,1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            minW = 0.1*cam.get(3)
            minH = 0.1*cam.get(4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            faces = self.face_classifier.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH))
            )

            
            for (x,y,w,h) in faces:
                
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 2)
        
                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
                
                confidenceStr = "  {0}%".format(round(100 - confidence))
                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    user_id = id
                    name = self.database.retrieve_name(user_id)
                    cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)

                    if (confidence >= 70):
                        print(user_id)
                        self.database.insert_log(user_id)
                        
                else:
                    cv2.putText(img, "Unknown", (x+5,y-5), font, 1, (255,255,255), 2)
                    
                cv2.putText(img, str(confidenceStr), (x+5,y+h-5), font, 1, (255,255,0), 1)
                
            cv2.imshow('camera', img)
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        return user_id - 1
                    
    def train(self):
        faces, ids = self.getImagesAndLabels(self.data_path)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.write(self.trainer_file)
