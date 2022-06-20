import os
import sys
import random

def reprint(string):
    sys.stdout.write("\r")
    sys.stdout.write(string)
    sys.stdout.flush()

# GENERATE RANDOM KEY
randString = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
randName = ""
for n in range(5):
    randName += random.choice(randString)

print(randName)
print("\n >>> FILE RENAMER.PY")

#path = r"D:/Desktop/True Templates/True Earth/"
#path = r"D:/Desktop/Temp Templates/Temp Clouds/"
#path = r"D:/Desktop/True Templates/True Cloud/"

path = r"Images/"
path = r"True Templates/"

print (" Listing ...")

# CODE TO AVOID "FILE ALREADY EXISTS"
folderList = os.listdir(path)
z = 0

for folder in folderList:

    print(" Dir : " + str(folder))
    fileList = os.listdir(path + str(folder))

    for f in fileList:
        os.rename(path + str(folder + "/")+ str(f), path + str(folder + "/") + randName + str(z) + ".jpg")
        z += 1

# REAL CODE
print("")
for folder in folderList:

    folder = str(folder)
    fileList = os.listdir(path + str(folder))
    nFiles = len(os.listdir(path + str(folder)))
    i = 0

    print("")
    for f in fileList:
        os.rename(path + str(folder + "/") + str(f), path + str(folder + "/") + str(folder) + "_" + str(i) + ".jpg")
        reprint(" DIR " + str(folder) + "---> Loaded : " + str(i) + "/" + str(nFiles))
        i += 1


    

print("\n DONE !\n")

input("Press key to continue . . .")