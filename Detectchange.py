import cv2
import sys
import numpy as np
import pygame as py

# Constant

W,H = 720,450
ERROR = 30
CAMERA_WIGHT = 48
PART = 6
CAMERA_HIGH = int(CAMERA_WIGHT*0.75) # 36
BLOCK_WIGHT = int(W/CAMERA_WIGHT)
fps = 1
clock = py.time.Clock()

before = np.zeros((CAMERA_WIGHT,CAMERA_HIGH,3), np.uint8)

# Init

cap = cv2.VideoCapture(0)

# Camera read

def read():
    ret,frame = cap.read()
    return np.rot90(cv2.resize(frame, (CAMERA_WIGHT,CAMERA_HIGH))),frame

# Detect Move

def detect(img1,img2):
    move = np.abs(img1 - img2)
    move = np.all((ERROR > move) | (move > 255 - ERROR), axis=2).astype(int)

    x,y = move.shape
    a = []

    for i in range(0,x,PART):
        for j in range(0,y,PART):
            block = move[i:i+PART, j:j+PART].flatten()
            average = round(np.mean(block),3)
            a.append(average)

    b = np.array(a).reshape(x//PART,y//PART)
    b = np.rot90(np.flipud(b))
    print(b)
    return b

# Main loop

while True:
    
    img , frame= read()

    detect(img,before)

    before = img

    clock.tick(fps)