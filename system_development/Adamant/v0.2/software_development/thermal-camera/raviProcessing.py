import time 
import functionFIles as bruh

bruh.clear_terminal()

inputPath = r"C:\Users\mayhe\OneDrive\Documents\Thermal stuff\3_13_2026"
outputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\In-situ-monitoring-of-powder-bed-fusion-additive-manufacturing\system_development\Adamant\v0.2\software_development\thermal-camera"

raviFileNames = bruh.gimmeFileNames(inputPath)
raviFiles = bruh.buildFilePaths(inputPath)

for i, file in enumerate(raviFileNames):
    print(f"{i}: {file}")
    capture = bruh.captureVideo(raviFiles[i])
    bruh.makeVideo(capture, outputPath, raviFileNames[i], True, 188, 90, 125, 125)

print("FINALLY DONE!")