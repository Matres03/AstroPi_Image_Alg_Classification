import cv2, numpy as np
from sklearn.cluster import KMeans
import os
from PIL import Image
import shutil
import time

def reprint(string):
    import sys
    sys.stdout.write("\r")
    sys.stdout.write(string)
    sys.stdout.flush()

img_list = []

Red_List = []
Green_List = []
Blue_List = []

c = 0
l = 0

# COUNT AND ADD .JPGs TO THE LIST
for subdir, dirs, files in os.walk("Frame/"):

    for f in files:

        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + f

        if filepath.endswith(".jpg"):
            #print (f)
            img_list.append(f)
            c += 1

print (" Found " + str(c) + " .jpg files...")

for f in img_list: 

    l += 1
    color_list = []
    perc_list = []

    reprint(" Progress : " + str(l) + " / " + str(c))
    time.sleep(0.4)
    img = Image.open("Frame/" + str(f))
    img = img.resize((300, 300))
    img.save("Frame/" + str(f))

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
        start = end

    Red_List.append(color_list[i-1][0])
    Green_List.append(color_list[i-1][1])
    Blue_List.append(color_list[i-1][2])

print ("\n DONE !")

print ("\n MAX : [ " + str(max(Red_List)) + ", " + str(max(Green_List)) + ", " + str(max(Blue_List)) + "]")
print (" MIN : [ " + str(min(Red_List)) + ", " + str(min(Green_List)) + ", " + str(min(Blue_List)) + "]")

print (" MEAN : ["+ str(sum(Red_List)/c) + ", " + str(sum(Green_List)/c) + ", " + str(sum(Blue_List)/c) + "]\n ")

if c == 1 : 
    print (perc_list[i - 1])
