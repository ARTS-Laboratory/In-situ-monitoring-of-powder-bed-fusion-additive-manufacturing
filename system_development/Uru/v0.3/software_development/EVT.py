#EVT.py
#By: Jackie Yang
#Supposedly a python automation to convert a .raw file from the event camera into a .csv file. Who knows

import subprocess
import os

###Helper Functions
def inp(text:str="", validResponses=[], outputType=str):
    while True:
        if len(validResponses) == 0:
            try:
                response = input(text)
                return outputType(response) #try catches this
            except ValueError:
                print("Invalid response, try again!")
        else:
            try:
                response = input(text)
                if response.lower() in validResponses: #i'm just assuming that the valid responses are in lowercase
                    return outputType(response.lower()) #it'll return the lowercase version of it
                else:
                    raise ValueError
            except ValueError:
                print("Invalid response, try again!")

def getFile(fileType,text=""):
    while True:
        inp = input(text).strip("\"") #assuming that your file name doesn't have " on them
        try:
            if os.path.exists(inp) and os.path.splitext(inp)[-1].lower() == fileType:
                return inp
            elif fileType == "folder" and os.path.isdir(inp): #user will have to use this parameter. previous attempt was using a bool parameter
                return inp
            else:
                raise Exception("File cannot be found, try again") #no idea
        except:
            print("Invalid file! Try again!")

###Code
if inp("Are your paths default?\nyes or no: ",["yes","no"]) == "yes":
    csvLocation = "C:\\Users\\CBUREN\\Desktop\\Metavision\\CSV"
    exeFile = "C:\\Users\\CBUREN\\Documents\\GitHub\\openeb\\build\\bin\\Release\\metavision_evt3_raw_file_decoder.exe"
    rawFile = getFile(".raw","Enter the raw file: ")
else:
    csvLocation = getFile("folder","Enter the folder where the .csv file will be located: ")
    exeFile = getFile(".exe","Enter the exe file: ")
    rawFile = getFile(".raw","Enter the raw file: ")

csvFile = inp("Name your .csv file: ") + ".csv"

os.chdir(csvLocation)
print("New directory: ", os.getcwd())

command = subprocess.run(["powershell","-Command",exeFile,rawFile,csvFile],capture_output=True,text=True)
