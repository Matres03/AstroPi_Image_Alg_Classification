import sys
import cv2, numpy as np
from sklearn.cluster import KMeans
import os
from PIL import Image
import shutil
import time
from timeit import default_timer as timer
import math

# EXT FUNCTIONS
def renameFolderFiles(path, prefix) :

    # avoid dup files error
    path = str(path)
    prefix = str(prefix)
    fileList = os.listdir(path)
    i = 0

    for f in fileList:
        os.rename(path + str(f), path + "_" + str(i) + ".jpg")
        i += 1

    i = 0
    fileList = os.listdir(path)
    for f in fileList:
        os.rename(path + str(f), path + prefix + "_" + str(i) + ".jpg")
        i += 1
    
    print("Renamed all files in folder : " + str(path) + " !")

def truncate(number, digits) -> float:

    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def between(left, value, right):

    if value < right and value > left:
        return True;
    else :
        return False;

def reprint(string):
    import sys
    sys.stdout.write("\r")
    sys.stdout.write(string)
    sys.stdout.flush()

# DEF VARIABLES
img_list = []
deltaRList = []
fileN = 0
times = 0

# CALC TOTOL IMAGES AMOUNT
# CREATE LIST OF IMAGES NAME
for subdir, dirs, files in os.walk("Frame/"):

    for f in files:

        #reprint os.path.join(subdir, file)
        filepath = subdir + os.sep + f

        if filepath.endswith(".jpg"):
            #reprint (f)
            img_list.append(f)
            fileN += 1

reprint ("\nFOUND " + str(fileN) + " .jpg files...\n")

#square = int(input("Insert Resize resolution : "))
square = 200
delay = 0.4

# START CYCLE
for f in img_list: 

    try:
        times += 1

        time.sleep(delay)
        end = timer()
        speed = end / times ;
        frac, whole = math.modf((fileN - times)/(speed * 60)) # time left
        print(str(times) + "/" + str(fileN))
    
        img = Image.open("Frame/" + str(f))
        img = img.resize((square, square))
        img.save("Frame/" + str(f))

        colorList = []
        percList = []
        rList = []
        gList = []
        bList = []

        image = cv2.imread('Frame/' + str(f))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        reshape = image.reshape((image.shape[0] * image.shape[1], 3))
        cluster = KMeans(n_clusters=5).fit(reshape)
        centroids = cluster.cluster_centers_

        labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        (hist, _) = np.histogram(cluster.labels_, bins = labels)
        hist = hist.astype("float")
        hist /= hist.sum()

        # Create frequency rect and iterate through each cluster's color and percentage
        #rect = np.zeros((50, 300, 3), dtype=np.uint8)

        colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
        i = 0
        start = 0

        for (percent, color) in colors:
            i += 1
            #reprint(color, "{:0.2f}%".format(percent * 100))

            # COLOR PERCENTAGE
            value = float("{:0.2f}".format(percent * 100))

            colorList.append(color)
            percList.append(value)
            rList.append(color[0])
            gList.append(color[1])
            bList.append(color[2])
            #reprint(value)

            end = start + (percent * 300)
            start = end

        p2 = (percList[i-2]*100/percList[i-1]) /100
        #reprint(p2)
        rMean = (rList[i-1] + rList[i-2]*p2) / (1+p2)
        gMean = (gList[i-1] + gList[i-2]*p2) / (1+p2)
        bMean = (bList[i-1] + bList[i-2]*p2) / (1+p2)
        last2mean = [rMean, gMean, bMean]


        # BLUE
        deltaB = bMean - (rMean + gMean) / 2 

        # GREY
        lightLevel = (rMean + gMean + bMean)/3
        var = math.sqrt((pow(rMean - lightLevel,2) + pow(gMean - lightLevel,2) + pow(bMean - lightLevel,2))/3.0)

        # SEA
        blueImp = deltaB*var

        # RED
        deltaR = (rMean - (gMean + bMean - deltaB)/2)
        deltaRList.append(deltaR)
    

        print ("")

        if deltaB < -8 :
            print(f)
            print("NO SIGNAL")

        elif lightLevel < 12:
            print(f)
            print("NIGHT")

        elif deltaB > 18 and var > 10 and lightLevel > 40:
            print(f)
            print("SEA")

        elif deltaR > -1:
            print(f)
            print("EARTH")

        elif lightLevel < 45 or between(-0.6, deltaR, 0.7):
            print(f)
            print("SUN SET-RISE")

        elif var < 10 :
            print(f)
            print("CLOUD")

        else:
            print(f)
            print("DAY")

        print("Blue Diff   : " + str(deltaB))
        print("Blue Imp    : " + str(blueImp))
        print("Red  Diff   : " + str(deltaR))
        print("Light Level : " + str(lightLevel))
        print("Grey Diff   : " + str(truncate(var,1)))
        #input()

    except Exception as err:
        print("ERROR ON :" + str(f))
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        pass

print("\nDeltaRList : ")

for r in deltaRList:
    print(" > " + str(r))

print("\n DONE !\n")  