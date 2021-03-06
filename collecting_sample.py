import cv2
import numpy as np
import os
import time
import sys

def collectingsamples(criminal_name,criminal_ID):


    dir_path = '/home/osboxes/PycharmProjects/Face-Detection-and-Recognition/datasets/'+str(criminal_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        print('[INFO] Already exist')
        overwrite=int(input("Do, You want to overwrite it! \nfor Yes, press 1 \nfor No, press any key\n"))

        if overwrite == 1:
            print("[INFO] Process Started....Rewriting the faces")
        else:
            criminal_name_again = str(input('Enter criminal name:\t'))
            collectingsamples(criminal_name_again)

    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def face_extractor(img):
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray_img,scaleFactor=1.3,minNeighbors=5)#extract faces

        if faces == ():
            return None

        for(x,y,w,h) in faces:
            cropped_face = img[y:y+h,x:x+w]

        return  cropped_face


    cap = cv2.VideoCapture(0)
    count = 0

    # Loading Bar
    def progressbar(it, prefix="", size=60, file=sys.stdout):
        count = len(it)

        def show(j):
            x = int(size * j / count)
            file.write("%s[%s%s] %i/%i\r" % (prefix, "#" * x, "." * (size - x), j, count))
            file.flush()

        show(0)
        for i, item in enumerate(it):
            yield item
            show(i + 1)
        file.write("\n")
        file.flush()


    while True:
        ret,frame = cap.read()
        if face_extractor(frame) is not None:
            count+=1
            face = cv2.resize(face_extractor(frame),(200,200))#fixing the image_size
            face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)

            cv2.imwrite(dir_path+"/"+str(criminal_name)+
                        '.'+ str(criminal_ID) + '.' +
                        str(count) + ".jpg", face)

            cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.imshow('Face Extractor',face)

        else:
            print("Face Not Found")
            pass

        if cv2.waitKey(1)==13 or count == 25:
            break


    cap.release()
    cv2.destroyAllWindows()
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")

    for i in progressbar(range(25), "Processing: ", 40):
        time.sleep(0.3)  # any calculation you need

    print("Collecting samples completed")