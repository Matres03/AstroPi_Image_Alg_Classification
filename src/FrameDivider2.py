import cv2, numpy as np
import os
import shutil
import math
import sys
import time
from sklearn.cluster import KMeans
from PIL import Image

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

# VARS
folderPath = "Images/toDivide/"
img_list = []
delay = 0.3
c = 0
l = 0

# START LOG
print("\n >>> FrameDivider 2.0 launched! ")

# LISTS DIR 
for subdir, dirs, files in os.walk(folderPath):

    for f in files:
        
        filepath = subdir + os.sep + f

        if filepath.endswith(".jpg"):
            img_list.append(f)
            c += 1

print ("\n " + str(c) + " .jpg files were found!\n")

# CYCLES TROUGH THE IMGs LIST
for f in img_list: 

    try:
        time.sleep(delay)
        # CYCLE LOG UPDATE
        l += 1
        reprint(" LOADING " + str(l) + "/" + str(c))

        # IMAGE SELECTION AND RESIZE
        img = Image.open(folderPath + str(f))
        img = img.resize((200, 200))
        img.save(folderPath + str(f))

        # CHECK FOR LOW RES
        if (os.path.getsize(folderPath + f) < 2600):
            shutil.move(folderPath + f, "Images/NDEF" )
            continue

        # IMAGE COLOR ANALISYS
        image = cv2.imread(folderPath + str(f))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        reshape = image.reshape((image.shape[0] * image.shape[1], 3))
        cluster = KMeans(n_clusters=5).fit(reshape)
        centroids = cluster.cluster_centers_
        labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        (hist, _) = np.histogram(cluster.labels_, bins = labels)
        hist = hist.astype("float")
        hist /= hist.sum()

        # COLOR SORTING
        colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
    
        i = 0

        # RETURNS FRAME CLASSIFICATION PERC
        for (percent, color) in colors:

            i += 1

            # COLOR PERCENTAGE
            percList = []
            EarthPerc = 0
            SeaPerc = 0
            DarkPerc = 0
            DawnPerc = 0
            CloudsPerc = 0

            # IMAGE STUFF
            labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
            (hist, _) = np.histogram(cluster.labels_, bins = labels)
            hist = hist.astype("float")
            hist /= hist.sum()
    
            # RECTANGLE PALETTE
            rect = np.zeros((50, 300, 3), dtype=np.uint8)
            colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
            start = 0

            # COLOR PERCENTAGE
            perc = float("{:0.2f}".format(percent * 100))
            #print("\n-----------------------------------------------------------------------")
            #print (" COLOR " + str(color) + " --> PERC [" + str(perc) + " %]") 

            r = color[0]
            g = color[1]
            b = color[2]

            # BLUE
            deltaB = b - (r + g) / 2 
            # GREY
            lightLevel = (r + g + b)/3
            greyDiff = math.sqrt((pow(r - lightLevel,2) + pow(g - lightLevel,2) + pow(b - lightLevel,2))/3.0)

            # RED
            deltaR = (r - (g + b - deltaB)/2)

            #print("\n\tBlue Diff   : " + str(deltaB))
            #print("\tRed  Diff   : " + str(deltaR))
            #print("\tLight Level : " + str(lightLevel))
            #print("\tGrey Diff   : " + str(truncate(greyDiff,1)))

        if lightLevel < 22:
            #print("\n\tDARK ")
            DarkPerc += perc

        else :

            if deltaB > 20 and deltaR < -5:
                #print("\n\tSEA ")
                SeaPerc += perc

            elif deltaR > -1:
                #print("\n\tEARTH ")
                EarthPerc += perc

            elif greyDiff < 10 and lightLevel > 130:
                #print("\n\tCLOUDS ")
                CloudsPerc += perc

            else :
                #print("\n\tCLOUDS ")
                CloudsPerc += perc

        percList.append(DarkPerc)       #0
        percList.append(SeaPerc)        #1
        percList.append(CloudsPerc)     #2
        percList.append(EarthPerc)      #3
        percList.append(DawnPerc)       #4

        print("\n Dark : " + str(percList[0]))
        print(" Sea : " + str(percList[1]))
        print(" Cloud : " + str(percList[2]))
        print(" Earth : " + str(percList[3]))
        print(" Dawn : " + str(percList[4]))
        print("\n")

        index = percList.index(max(percList))

        if DarkPerc > 30 :
            shutil.move(folderPath + f, "Images/Night" )

        elif EarthPerc > 30 and SeaPerc > 30 and CloudsPerc > 30:
            shutil.move(folderPath + f, "Images/Doubt" )

        elif EarthPerc > 40:
            shutil.move(folderPath + f, "Images/Earth" )

        elif index == 1:
            shutil.move(folderPath + f, "Images/Sea" )

        elif index == 2:
            shutil.move(folderPath + f, "Images/Cloud" )

        elif index == 3:
            shutil.move(folderPath + f, "Images/Earth" )

        else:
            shutil.move(folderPath + f, "Images/NoSignal" )
        input()

    except Exception as err:
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        shutil.move(folderPath + f, "Images/ERROR" )
        pass

#os.system("shutdown /s /t 1")