import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = './user_image'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("./opencv_data/haarcascade/haarcascade_frontalface_default.xml");

# function to get the images and label data
def getImagesAndLabels(path):

    dictionary = {}
    
    for folder in os.listdir(path):
        fullPath = os.path.join(path,folder)
        dictionary[folder] = [os.path.join(fullPath, image) for image in os.listdir(fullPath)]
        
    faceSamples=[]
    ids = []

    for name,imagePaths in dictionary.items():
        print(name)
        print(imagePaths)
        PIL_imgs = [Image.open(imagePath) for imagePath in imagePaths] # convert it to grayscale
        imgs_numpy = [np.array(PIL_img,'uint8') for PIL_img in PIL_imgs]

        for img_numpy in imgs_numpy:
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(int(name))

    return faceSamples,ids

#dict = {}
#for folder in os.listdir(path):
#    imagePaths = [image for image in os.listdir(os.path.join(path,folder))]
#    dict[folder] = imagePaths


#print(dict)
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('./opencv_data/trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
