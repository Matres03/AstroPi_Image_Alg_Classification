
import math
import cv2, numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import KDTree

class ImageData:
    sea = False;
    earth = False;
    clouds = False;
    dark = False;

def truncate(number, digits) -> float:

    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def between(left, value, right):

    if value < right and value > left:
        return True;
    else :
        return False;

def visualize_colors(cluster, centroids):
    
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

    # ITERATE TROUGH COLORS
    for (percent, color) in colors:
        
        # COLOR PERCENTAGE
        perc = float("{:0.2f}".format(percent * 100))
        print("\n-----------------------------------------------------------------------")
        print (" COLOR " + str(color) + " --> PERC [" + str(perc) + " %]") 

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

        print("\n\tBlue Diff   : " + str(deltaB))
        print("\tRed  Diff   : " + str(deltaR))
        print("\tLight Level : " + str(lightLevel))
        print("\tGrey Diff   : " + str(truncate(greyDiff,1)))

        end = start + (percent * 300)
        cv2.rectangle(rect, (int(start), 0), (int(end), 50), \
                      color.astype("uint8").tolist(), -1)
        start = end

        if lightLevel < 22:
            print("\n\tDARK ")
            DarkPerc += perc
        else :

            if deltaB > 20 and deltaR < -5:
                print("\n\tSEA ")
                SeaPerc += perc

            elif deltaR > 0:
                print("\n\tEARTH ")
                EarthPerc += perc

            elif greyDiff < 10 and lightLevel > 130:
                print("\n\tCLOUDS ")
                CloudsPerc += perc

            #elif deltaR > -6 and between(60, lightLevel, 100): 
                #print("\n\tEARTH ")
                #EarthPerc += perc

            else :
                print("\n\tCLOUDS ")
                CloudsPerc += perc

        print("\n    PERCENTAGE LIST : ")
        print ("\tEarth  : " + str(EarthPerc) + "%")
        print ("\tSea    : " + str(SeaPerc) + "%")
        print ("\tClouds : " + str(CloudsPerc) + "%")
        print ("\tDawn   : " + str(DawnPerc) + "%")
        print ("\tDark   : " + str(DarkPerc) + "%")

    return rect

# Load image and convert to a list of pixels
image = cv2.imread('Images/toDivide/SunSetRise_7952.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
reshape = image.reshape((image.shape[0] * image.shape[1], 3))

# Find and display most dominant colors
cluster = KMeans(n_clusters=5).fit(reshape)
visualize = visualize_colors(cluster, cluster.cluster_centers_)
visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
cv2.imshow('Palette', visualize)
cv2.waitKey()

