#from sys import last_traceback
import cv2, numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import os
import math

import numpy as np
import PIL
from PIL import Image
from PIL import ImageEnhance

def between(left, value, right):

    if value < right and value > left:
        return True;
    else :
        return False;

def visualize_colors(cluster, centroids):

    i = 0
    colorList = []
    percList = []

    rList = []
    gList = []
    bList = []

    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()

    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((50, 300, 3), dtype=np.uint8)
    colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
    start = 0
    for (percent, color) in colors:

        i += 1
        # COLOR PERCENTAGE
        print(color, "{:0.2f}%".format(percent * 100))
        colorList.append(color)
        rList.append(color[0])
        gList.append(color[1])
        bList.append(color[2])

        # COLOR PERC
        value = float("{:0.2f}".format(percent * 100))
        percList.append(value/100)
        #print(value)

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

        print("\tDelta B : " + str(deltaB) )
        print("\tLight Level : " + str(lightLevel) )
        print("\tgreyDiff : " + str(greyDiff) )
        print("\tDelta R : " + str(deltaR) + "\n")

        end = start + (percent * 300)
        cv2.rectangle(rect, (int(start), 0), (int(end), 50), \
                      color.astype("uint8").tolist(), -1)
        start = end

    #after the calculations
    p2 = (percList[i-2]*100/percList[i-1]) /100
    print(p2)
    rMean = (rList[i-1] + rList[i-2]*p2) / (1+p2)
    gMean = (gList[i-1] + gList[i-2]*p2) / (1+p2)
    bMean = (bList[i-1] + bList[i-2]*p2) / (1+p2)
    mean = (rMean + gMean + bMean)/3
    var = (rMean - mean + gMean - mean + bMean - mean)/3.0

    last2mean = [rMean, gMean, bMean]
    deltaB = bMean - (rMean + gMean) / 2 
    greyValue = (rMean + gMean + bMean)/bMean
    lightLevel = (rMean + gMean + bMean)/(3)

    print("Mean        : " + str(last2mean))
    print("Delta Blue  : " + str(deltaB)) 
    print("Grey Value  : " + str(var)) 
    print("Light Level : " + str(lightLevel))

    return rect

img = PIL.Image.open('Images/toDivide/TrueEarth_27.jpg')
converter = PIL.ImageEnhance.Sharpness(img)
img2 = converter.enhance(1) #sharpness
converter = PIL.ImageEnhance.Contrast(img)
img = converter.enhance(2.5)  #contrasto
converter = PIL.ImageEnhance.Color(img)
img2 = converter.enhance(2) #saturazione
#img.show()  #mostyra imm originale
#img2.show() #mostra immagine modificata
img.save("Images/toDivide/Test2_TrueEarth_27.jpg")
img2.save("Images/toDivide/Test1_TrueEarth_27.jpg")

# IMG PATH
path = 'Images/toDivide/Test2_TrueEarth_27.jpg'

# Load image and convert to a list of pixels
image = cv2.imread(path)
print("\n Img file size:" + str(os.path.getsize(path)))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
reshape = image.reshape((image.shape[0] * image.shape[1], 3))

# Find and display most dominant colors
cluster = KMeans(n_clusters=5).fit(reshape)
visualize = visualize_colors(cluster, cluster.cluster_centers_)
visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
cv2.imshow('Palette', visualize)
cv2.waitKey()

