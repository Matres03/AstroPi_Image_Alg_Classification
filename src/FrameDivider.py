import cv2, numpy as np
from sklearn.cluster import KMeans
import os
from PIL import Image
import shutil
import time
from timeit import default_timer as timer
import math

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
c = 0
l = 0

for subdir, dirs, files in os.walk("Frame/"):

    for f in files:

        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + f

        if filepath.endswith(".jpg"):
            #print (f)
            img_list.append(f)
            c += 1

print ("Found " + str(c) + " .jpg files...")

#print(img_list)

delay = 0.4

for f in img_list: 

    l += 1

    time.sleep(delay)
    end = timer()
    speed = end / l ;
    frac, whole = math.modf((c - l)/(speed * 60)) # time left
    reprint(str(l) + "/" + str(c) + " Time left : " + str(whole) + " m " + str(truncate(frac*60,0)) + " s")
    
    img = Image.open("Frame/" + str(f))
    img = img.resize((200, 200))
    img.save("Frame/" + str(f))

    color_list = []
    perc_list = []
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
    start = 0

    #print ("\nLOADED IMAGE : " + str(f) + " ...")

    i = 0

    for (percent, color) in colors:
        i += 1
        #print(color, "{:0.2f}%".format(percent * 100))

        # COLOR PERCENTAGE
        value = float("{:0.2f}".format(percent * 100))
        color_list.append(color)
        perc_list.append(value)
        #print(value)

        end = start + (percent * 300)
        #cv2.rectangle(rect, (int(start), 0), (int(end), 50), \
                      #color.astype("uint8").tolist(), -1)
        start = end

    #print(color_list[i-1])

    mean = (color_list[i-1][0] + color_list[i-1][1] + color_list[i-1][2])/3 
    #print (mean)

    if color_list[i-1][0] < 13 and color_list[i-1][1] < 1 and color_list[i-1][2] < 6 :
        
        shutil.move("Frame/" + f, "Night" )
        #print(f + " ---> Moved to '\\Night'")

    elif color_list[i-1][0] < 11 and color_list[i-1][1] < 3 and color_list[i-1][2] < 3 :

        shutil.move("Frame/" + f, "No_Signal" )
        #print(f + " --- >Moved to '\\No_Signal'")

    elif between(mean - 20, color_list[i-1][0], mean + 20) and between(mean - 20, color_list[i-1][1], mean + 20) and between(mean - 20, color_list[i-1][2], mean + 20) and mean > 135:
        #print(" " + str(f) + " IS A CLOUD!")
        shutil.move("Frame/" + f, "Cloud" )

    else:
        shutil.move("Frame/" + f, "Day" )