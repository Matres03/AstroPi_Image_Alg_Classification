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

path = r"D:/Desktop/True Templates/True Night/"
prefix = "tNight"

print (" Listing ...")

# CODE TO AVOID "FILE ALREADY EXISTS"
fileList = os.listdir(path)
z = 0
for f in fileList:
    os.rename(path + str(f), path + randName + str(z) + ".jpg")
    z += 1

# REAL CODE
fileList = os.listdir(path)
nFiles = len(os.listdir(path))
i =0
c = 0

for f in fileList:
    os.rename(path + str(f), path + prefix + "_" + str(i) + ".jpg")
    i += 1
    c += 1
    reprint(" Loaded : " + str(c) + "/" + str(nFiles))

print("\n DONE !\n")

input("Press key to continue . . .")