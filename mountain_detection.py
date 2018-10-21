#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial
import os
import tkinter.filedialog
import tkinter as Tk
from tkinter import *
from pygame import mixer
from PIL import Image, ImageTk

mixer.init()
mixer.music.load('goodPlace.mp3')

#serial read
ser=serial.Serial(" COM11", 9600)
s = ser.read()

# In[2]:


win = Tk()
win.title('Mars Feng Shui detector')
win.geometry('800x600')

label = Label(win, text = '風水 Feng Shui', bg="yellow")
label.config(width=200)
label.config(font=("Courier", 50))
label.pack()

label = Label(win, text = '開啟所要評分圖片並連接感測器')
label.config(width=200)
label.config(font=("Courier", 30))
label.pack()


# In[3]:


img = cv2.imread(tkinter.filedialog.askopenfilename(),0)
#img = ImageTk.PhotoImage(Image.open(tkinter.filedialog.askopenfilename()))
img = cv2.resize(img, (1000, 600))

#plt.imshow(img,'gray')
#cv2.imwrite("C:\\Users\\mende\\Downloads\\Mars Feng Shui detector\\detect_result\\raw.jpg", img)

blurred = cv2.GaussianBlur(img, (11, 11), 10)
#plt.imshow(blurred,'gray')
#cv2.imwrite("C:\\Users\\mende\\Downloads\\Mars Feng Shui detector\\detect_result\\blurred.jpg", blurred)

ret,blur_bin= cv2.threshold(blurred,160,255,cv2.THRESH_BINARY)
#plt.imshow(blur_bin,'gray')
#cv2.imwrite("C:\\Users\\mende\\Downloads\\Mars Feng Shui detector\\detect_result\\bin.jpg", blur_bin)


# In[4]:


img_array = np.array(blur_bin)

'''
print("the size of image is")
print(img_array.shape)
print()
'''

#find the horizon and tag as 10
for x in range(img_array.shape[1]-1):
    for y in range(img_array.shape[0]-1):
        if img_array[y,x]==0:
            img_array[y,x] = 100
            break
#print(img_array)
print()

#create a array only shows the horizon
horizon_avg = 0
horizon = np.zeros(img_array.shape)
for x in range(horizon.shape[1]):
    for y in range(horizon.shape[0]):
        if img_array[y,x]==100:
            horizon_avg += y
            horizon[y:y+10,x] = 255
            break

#split(horizon, 4)
section = int(horizon.shape[1]/4)
north = horizon[:, 0:section]
east  = horizon[:, section:2*section]
south = horizon[:, 2*section:3*section]
west  = horizon[:, 3*section:4*section]

north_avg = 0
east_avg = 0
south_avg = 0
west_avg = 0

for x in range(north.shape[1]):
    for y in range(north.shape[0]):
        if north[y,x]==255:
            north_avg += y
north_avg /= north.shape[1]*3
            
for x in range(east.shape[1]):
    for y in range(east.shape[0]):
        if east[y,x]==255:
            east_avg += y
east_avg /= east.shape[1]*3
            
for x in range(south.shape[1]):
    for y in range(south.shape[0]):
        if south[y,x]==255:
            south_avg += y
south_avg /= south.shape[1]*3
            
for x in range(west.shape[1]):
    for y in range(west.shape[0]):
        if west[y,x]==255:
            west_avg += y  
west_avg /= west.shape[1]*3

#calculate the total score
mountain_score = ((south_avg-north_avg)*15+(south_avg-east_avg)*13+(south_avg-west_avg)*10)/south_avg*20

'''
print(north_avg)
print(east_avg)
print(south_avg)
print(west_avg)

mars_horizon = Image.fromarray(horizon)
plt.imshow(mars_horizon)
plt.show()
'''

print("score:")
print(mountain_score)

total_score = mountain_score + s
if total_score > 7:
    mixer.music.play()
    goodplace = cv2.imread('ogoodplace.jpg')
    plt.imshow(cv2.cvtColor(goodplace, cv2.COLOR_BGR2RGB))
    plt.show()
else:
    nogoodplace = cv2.imread('nogoodplace.jpg')
    plt.imshow(cv2.cvtColor(nogoodplace, cv2.COLOR_BGR2RGB))
    plt.show()
    
win.mainloop()
    
#os.system("pause")


# In[ ]:




