import subprocess
import os

##### Defs
def code_cleaner(old_PS_code_combo):
    combo_PS_code = ' '.join(old_PS_code_combo)
    cleaner = combo_PS_code.replace(',','').replace("'","").replace("(","").replace(")","")
    return cleaner

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    return completed

def getFile(fileType,text=""):
    while True:
        inp = input(text).strip("\"") #assuming that your file name doesn't have " on them
        if os.path.exists(inp) and os.path.splitext(inp)[-1].lower() == fileType:
            return inp
        else:
            print("Something's wrong, try again.")
        
##### Printing
##### Defult Locations
file_answer = input("Are you files in the expected location?\nNote: must be the exact same as mine and type yes or no\n")

if file_answer.lower() == "yes":
    evt3_answer = input("Do you want to convert .raw into evt3.0? ")

    if evt3_answer.lower() == "yes":
        new_exe = getFile(".raw","Enter the file path: ")
    else:
        new_exe = getFile(".exe","First copy the path of the .exe file you want to use: ")
else:
    new_exe = getFile(".exe","First copy the path of the .exe file you want to use: ")

# output location (if needed .replace("\\","\\\\"))

csv_location_unclean = input("What folder do you want the excel file in? ")
csv_location = csv_location_unclean.replace('"','')
os.chdir(csv_location)
print("New directory: ", os.getcwd())

print("\nEnsure that all the paths are absolute not relative")

# .exe
new_exe = getFile(".exe","First copy the path of the .exe file you want to use: ")

# .raw
new_raw = getFile(".raw","Next where is the .raw file located:")

# excel file
excel = input("What do you want to name the excel file: ") + ".csv"

old_PS_code = (new_exe, new_raw, excel)

new_PS_code = code_cleaner(old_PS_code)
print(new_PS_code)

##### CMD
PS_code = run(new_PS_code)
if PS_code.returncode != 0:
    print("An error occured: %s", PS_code.stderr)
else:
    print(".csv made successfully!")