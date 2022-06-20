import sys
import cv2, numpy as np
from sklearn.cluster import KMeans
import os
from PIL import Image
import shutil
import time
from timeit import default_timer as timer
import math

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

img_list = []
fileN = 0
times = 0

renameFolderFiles("Frame/", "frame")

for subdir, dirs, files in os.walk("Frame/"):

    for f in files:

        #reprint os.path.join(subdir, file)
        filepath = subdir + os.sep + f

        if filepath.endswith(".jpg"):
            #reprint (f)
            img_list.append(f)
            fileN += 1

print ("\nFOUND " + str(fileN) + " .jpg files...\n")

square = int(input("Insert Resize resolution : "))
delay = 0.4

folderNameList = ["Night", "Day", "Cloud", "SunSetOrRise", "Sea"]
for folderName in folderNameList :
    renameFolderFiles(folderName + "/", folderName)


n = len(os.listdir("NoSignal/")) + 1
b = len(os.listdir("Night/")) + 1
c = len(os.listdir("Cloud/")) + 1
o = len(os.listdir("SunSetOrRise/")) + 1
s = len(os.listdir("Sea/")) + 1
l = len(os.listdir("LowLight/")) + 1
e = len(os.listdir("Earth/")) + 1
d = len(os.listdir("Day/")) + 1
# rename files to avoid errors

for f in img_list: 

    times += 1

    time.sleep(delay)
    end = timer()
    speed = end / times ;
    frac, whole = math.modf((fileN - times)/(speed * 60)) # time left
    #rereprint(str(l) + "/" + str(c) + " Time left : " + str(whole) + " m " + str(truncate(frac*60,0)) + " s")
    print("\n" + str(times) + "/" + str(fileN) + " Time left : " + str(whole) + " m " + str(truncate(frac*60,0)) + " s")
    print(f)
    img = Image.open("Frame/" + str(f))
    img = img.resize((square, square))
    img.save("Frame/" + str(f))

    colorList = []
    percList = []
    rList = []
    gList = []
    bList = []
    deltaRList = 0

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
    try:
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
        
        # MEANS
        rMean = (rList[i-1] + rList[i-2]*p2) / (1+p2)
        gMean = (gList[i-1] + gList[i-2]*p2) / (1+p2)
        bMean = (bList[i-1] + bList[i-2]*p2) / (1+p2)
        last2mean = [rMean, gMean, bMean]

        # LIGHT
        lightLevel = (rMean + gMean + bMean)/3

        # SEA
        deltaB = bMean - (rMean + gMean) / 2 
        
        # CLOUD
        var = math.sqrt((pow(rMean - lightLevel,2) + pow(gMean - lightLevel,2) + pow(bMean - lightLevel,2))/3.0)

        # EARTH
        deltaR = (rMean - (gMean + bMean - deltaB)/2)

        if deltaB < -8 :
            n += 1
            print("NO SIGNAL")
            shutil.move("Frame/" + f, "NoSignal" )
            os.rename("NoSignal/" + str(f), "NoSignal/NoSignal_" + str(n) + ".jpg")

        elif lightLevel < 12:
            b += 1
            print("NIGHT")
            shutil.move("Frame/" + f, "Night" )
            os.rename("Night/" + str(f), "Night/Night_" + str(b) + ".jpg")

        elif deltaB > 18 and var > 10 and lightLevel > 40:
            s += 1
            print("SEA")
            shutil.move("Frame/" + f, "Sea" )
            os.rename("Sea/" + str(f), "Sea/Sea_" + str(s) + ".jpg")

        elif deltaR > -1:
            e += 1
            print("EARTH")
            os.rename("Frame/" + str(f), "Frame/Earth_" + str(e) + ".jpg")
            shutil.move("Frame/Earth_" + str(e) + ".jpg", "Earth" )

        elif lightLevel < 45 :
            o += 1
            print("SUN SET-RISE")
            shutil.move("Frame/" + str(f), "SunSetOrRise" )
            os.rename("SunSetOrRise/" + str(f), "SunSetOrRise/SunSetOrRise_" + str(o) + ".jpg")

        elif var < 10 :
            c += 1
            print("CLOUD")
            os.rename("Frame/" + str(f), "Frame/Cloud_" + str(c) + ".jpg")
            shutil.move("Frame/Cloud_" + str(c) + ".jpg", "Cloud" )
            
        else:
            d += 1
            print("DAY")
            os.rename("Frame/" + str(f), "Frame/Day_" + str(d) + ".jpg")
            shutil.move("Frame/Day_" + str(d) + ".jpg", "Day" )

        #print("Blue Diff   : " + str(deltaB))
        #print("Red  Diff   : " + str(deltaR))
        #print("Light Level : " + str(lightLevel))
        #print("Grey Diff   : " + str(truncate(var,1)))
        #input()

    except Exception as err:
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        pass

print("")

print("\n DONE !\n")  