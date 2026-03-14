import os 
from pathlib import Path
import cv2
import numpy as np


def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def gimmeFileNames(path, includeFolders=False):
    folder = Path(path)
    if includeFolders:
        names = [item.name for item in folder.iterdir()]
    else:
        names = [file.name for file in folder.iterdir() if file.is_file()]
    return names

def buildFilePaths(path):
    fileNames = gimmeFileNames(path)
    filePath = []
    
    for files in fileNames:
        filePath.append(os.path.join(path, files))
        
    return filePath

def captureVideo(path):
    capture = cv2.VideoCapture(path)
    capture.set(cv2.CAP_PROP_CONVERT_RGB, -1)

    return capture

def readFrame(capture):
    ret, frame = capture.read()

    return ret, frame 
    
def makeVideo(capture, path, name, cropped, x, y, w, h):
    frameFolder = folderFind(path, name)
    count, fps, width, height = getVideoInfo(capture)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    colorWriter = cv2.VideoWriter(str(frameFolder / f"{name}.mp4"), fourcc, fps, (width, height), isColor=True)
    croppedWriter = cv2.VideoWriter(str(frameFolder / f"{name}Cropped.mp4"), fourcc, fps, (w, h), isColor=True)

    while True:
        ret, frame = readFrame(capture)
        if not ret:
            break
        
        frame = frame[:, :, 0].astype(np.uint16) | (frame[:, :, 1].astype(np.uint16) << 8)
        frame_roi = frame[1:, :]

        normalized = cv2.normalize(frame_roi, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        colored = cv2.applyColorMap(normalized, cv2.COLORMAP_INFERNO)
        cropped = cropROI(colored, x, y, w, h)
        
        croppedWriter.write(cropped)
        colorWriter.write(colored)
        count += 1
    
    colorWriter.release()
    print("Done!")

    
def folderFind(path, Name):
    folder = Path(path) / Name
    folder.mkdir(parents=True, exist_ok=True)
    
    return folder 

def getVideoInfo(capture):
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 30)
    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return frame_count, fps, width, height

def cropROI(frame, cx, cy, w, h):
    x = cx - w // 2
    y = cy - h // 2
    return frame[y:y+h, x:x+w]