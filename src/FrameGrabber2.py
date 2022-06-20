import cv2
import os, os.path
import pyautogui
import numpy as np
import math
import shutil
import time
from PIL import Image
from sklearn.cluster import KMeans
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def imgClass(f):

    square = 300

    # RESIZE
    img = Image.open(str(f))
    img = img.resize((square, square))
    img.save(str(f))
    img.close()

    colorList = []
    percList = []
    rList = []
    gList = []
    bList = []

    image = cv2.imread(str(f))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    reshape = image.reshape((image.shape[0] * image.shape[1], 3))
    cluster = KMeans(n_clusters=5).fit(reshape)
    centroids = cluster.cluster_centers_

    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()
    
    imgType = ""
    number = 0

    try:
        colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
        i = 0

        for (percent, color) in colors:
            i += 1
            value = float("{:0.2f}".format(percent * 100))

            colorList.append(color)
            percList.append(value)
            rList.append(color[0])
            gList.append(color[1])
            bList.append(color[2])

        p2 = (percList[i-2] *100/percList[i-1]) /100
        rMean = (rList[i-1] + rList[i-2]*p2) / (1+p2)
        gMean = (gList[i-1] + gList[i-2]*p2) / (1+p2)
        bMean = (bList[i-1] + bList[i-2]*p2) / (1+p2)
        
        deltaB = bMean - (rMean + gMean) / 2 
        lightLevel = (rMean + gMean + bMean)/3
        var = math.sqrt((pow(rMean - lightLevel,2) + pow(gMean - lightLevel,2) + pow(bMean - lightLevel,2))/3.0)


        if deltaB < -8 :
            imgType = "NOSIGNAL"

        elif lightLevel < 12:
            imgType = "NIGHT"

        elif deltaB > 18 and var > 10 and lightLevel > 40:
            imgType = "SEA"

        elif lightLevel < 45:
            imgType = "SUNSETRISE"

        elif var < 8 and lightLevel > 120 :
            imgType = "CLOUD"

        else:
            imgType = "DAY"

    except Exception:
        pass

    return [imgType, number]

dN = len(os.listdir("Day/"))
nN = len(os.listdir("Night/"))
sN = len(os.listdir("Sea/"))
cN = len(os.listdir("Cloud/"))
rN = len(os.listdir("SunSetOrRise/"))

i = len(os.listdir("Frame/"))
print (str(i) + " photo found ...")

with open('counter.txt', 'r+') as f:
    f.truncate(0)

with open('counter.txt', 'a') as f:
    f.write(str(i))

# Create local webserver and auto handles authentication.
gauth = GoogleAuth()           
drive = GoogleDrive(gauth)
gauth.LocalWebserverAuth()

while True:

    try:
        time.sleep(7)

        with open('counter.txt', 'r+') as f:
            i = int(f.read()) + 1
            f.truncate(0)

        with open('counter.txt', 'a') as f:
            f.write(str(i))

        # FRAME STR
        frame = 'frame_'+ str(i) + '.jpg'
        print("Frame : " + str(frame))
    
        # SAVE SCREEN
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("Frame/" + frame)
        img = Image.open("Frame/" + frame)

        # CROP PHOTO
        width, height = img.size
        img = img.crop((0+5,100,height-100+5,height))
        img.save("Frame/" + frame)
        img.close()

        # SELECT PHOTO TO UPLOAD
        upload_file = "Frame/" + frame

        # IMGs ClASSIFICATION
        imgType, counter = imgClass("Frame/" + frame);
        print ("Type : " + str(imgType))

        # GDRIVE DIR SELECTION
    
        if imgType == "DAY":

            dN += 1
            gfile = drive.CreateFile({'parents': [{'id': '1eg1EdYaL7ujVNT2nXNv4pozAKI0REyVb'}]})
            gfile['title'] = 'Day_' + str(dN) + '.jpg'
            gfile.SetContentFile(upload_file)
            gfile.Upload()
            gfile.content.close()
            shutil.move("Frame/" + frame, "Day" )
            os.rename("Day/" + str(frame), "Day/Day_" + str(dN) + ".jpg")

        elif imgType == "NIGHT":

            nN += 1
            gfile = drive.CreateFile({'parents': [{'id': '1hdmXxASZZuss8YShksPO-wQFiO5x_WEM'}]})
            gfile['title'] = 'Night_' + str(nN) + '.jpg'
            gfile.SetContentFile(upload_file)
            gfile.Upload()
            gfile.content.close()
            shutil.move("Frame/" + frame, "Night" )
            os.rename("Night/" + str(frame), "Night/Night_" + str(nN) + ".jpg")
    
        elif imgType == "SEA":

            sN += 1
            gfile = drive.CreateFile({'parents': [{'id': '10u2RlndQShe1ZyXVVyDik_Ki7h4hjVAh'}]})
            gfile['title'] = 'Sea_' + str(sN) + '.jpg'
            gfile.SetContentFile(upload_file)
            gfile.Upload()
            gfile.content.close()
            shutil.move("Frame/" + frame, "Sea" )
            os.rename("Sea/" + str(frame), "Sea/Sea_" + str(sN) + ".jpg")

        elif imgType == "CLOUD":

            cN += 1
            gfile = drive.CreateFile({'parents': [{'id': '1saDqx7vEDrz22W_ivkZ3RdsCAOOpbw4O'}]})
            gfile['title'] = 'Cloud_' + str(cN) + '.jpg'
            gfile.SetContentFile(upload_file)
            gfile.Upload()
            gfile.content.close()
            shutil.move("Frame/" + frame, "Cloud" )
            os.rename("Cloud/" + str(frame), "Cloud/Cloud_" + str(cN) + ".jpg")

        elif imgType == "SUNSETRISE":

            rN += 1
            gfile = drive.CreateFile({'parents': [{'id': '16Hp3MEgC29E2RGCWz1XAgTu5KkIXT6vx'}]})
            gfile['title'] = 'SunSetRise_' + str(rN) + '.jpg'
            gfile.SetContentFile(upload_file)
            gfile.Upload()
            gfile.content.close()
            shutil.move("Frame/" + frame, "SunSetOrRise" )
            os.rename("SunSetOrRise/" + str(frame), "SunSetOrRise/SunSetOrRise_" + str(rN) + ".jpg")

        # UPLOAD FILE
        if imgType != "NOSIGNAL":
            gfile.Upload()

        else:
            os.remove("Frame/" + frame)
    except Exception:
        pass