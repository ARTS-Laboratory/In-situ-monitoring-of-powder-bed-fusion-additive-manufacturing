'''
By: Charlie Buren
Date: 8/5/2025


Goals:
    - Make an menu to allow for selection of different .exe's 
    - Will allow for faster testing and better user expierence 

ToDo:
    1) 

Doc:
    - tkinter: https://docs.python.org/3/library/tkinter.html

'''

# --- Setup ---
# Import tkinter
from tkinter import * #imports GUI libary 
from tkinter import messagebox #imports messagebox which allows from stadard Tk dialog boxes
from tkinter import ttk #imports themeed widget sets which are newer than main tkinter
from tkinter import filedialog #allows for us to open a file

# Other
import subprocess
import os


## --- Defs ---
# Runs the code in PowerShell
def run_cmd(cmd): 
    try:
        if isinstance(cmd, list):
            completed = subprocess.run(cmd, capture_output=True, text=True)
        else:
            completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    except Exception as e:
        print(f'An error has occurred: {e}')
        # Assign a default value so return does not fail
        completed = None
    return completed

# Cleans up the generated lines of code to ensure no errors occur
def clean(cleaner):
     cleaner = cleaner.replace(',','').replace("'","").replace("(","").replace(")","").replace('"','')
     return cleaner

# --- Option defs ---
# Playback recordings
def mv_viewer_playback():
    PS_code = run_cmd('metavision_viewer.exe')
    return

# Convert .raw file to a .csv in the same location as the raw file
def raw_to_csv():
     # Path to raw to csv exe
     old_mv_csv_conv_path = "C:\\School\\Research\\GitHub\\openeb\\build\\bin\\Release\\metavision_evt3_raw_file_decoder.exe"
     mv_csv_conv_path = clean(old_mv_csv_conv_path)
     print(mv_csv_conv_path)

     # Select a file
     file_path = OpenFile()

     # Ensure that file has been selected. If no file has been selected then it runs again.
     try:
         file_path
     except:
         messagebox.showerror("File Selection Error. Try again.")
         return
     
     if file_path.lower().endswith(".raw"): # converts file path to lowercase and sees if ends with .raw. Ensures right file type has been selected
         # Create the .csv with the same name as .raw file
         created_csv = os.path.splitext(file_path)[0] + ".csv" #converts the path of the raw file and changes it to a .csv

         # Create the PS code
         cmd = [mv_csv_conv_path, file_path, created_csv] # combines the strings to create the code. Idk how it works it just does
         print(cmd) #testing

         # Run the PS code. This gives the errors or says if it works
         CodeRun = run_cmd(cmd)
         if CodeRun is None:
             messagebox.showerror("Error", "Failed to run command.")
             return
         elif CodeRun.returncode != 0:
             messagebox.showerror("Error", f"Command failed:\n{CodeRun.stderr}")
             return
         else:
             messagebox.showinfo("Success", "Conversion completed!")
             return
     else:
         messagebox.showerror("Please Select a .raw file")

# Catch the Check Button Event
def CheckButton(event):
    exe_selection = store_user_input.get() #.get() returns the value of the item with the specified key.
    messagebox.showinfo("Selection Menu", "You have selected the option: " + str(exe_selection)) #idk what it does but everyone had it like this

    #if statements
    if exe_selection == 'View recordings':
        mv_viewer_playback()
    elif exe_selection == 'Convert .raw file to .csv':
        raw_to_csv()
    # Error Line for errors or not completed options
    else: 
        messagebox.showinfo("Selection Menu", "Invalid selection:" + str(exe_selection))

# File selection
def OpenFile():
    file = filedialog.askopenfile(title="Select a file", # gives window opened a name
                                  filetypes=[("All files", "*.*")] # file types that can be selecteed
                                  ) 

    if file:
        global file_path #allows for file_path to be pulled anywhere in code
        file_path = file.name  # full file path as string
        file.close()  # Close the opened file (optional if you're not using it)

        file_name, file_extension = os.path.splitext(file_path)  # returns ('C:/path/to/file', '.xlsx')
        '''
        Note for testing. Also file_extension is what we need
        print("Full path:", file_path)
        print("File name:", file_name)
        print("File extension:", file_extension)
        '''
        #message box used for testing
        messagebox.showinfo("File Selected", f"Path: {file_path}\nType: {file_extension}")
        return file_path
    else:
        print("No file selected.") #allows for an error 



## --- Start Menu ---
# root setup
root = Tk() #root is toplevel menu. Root adds a seperate window that is the background I think. Its like opening a new tab I believe 
root.title("Uru Menu") #Adds a window title
root.geometry('200x300')

# list of all choices in the drop down menu
dropdown_choices = ['Stream from Camera (not working)', 
                    'View recordings', 
                    'Convert .raw file to .csv'] 

# String Stores user selection
store_user_input = StringVar() 

# Creation of menu labels
menu_label = Label(root, text = 'Select an .exe')
menu_label.pack(anchor = W, padx = 10, pady = 10) #padx or pady desinates teh exteral padding on each side. That means how big will it be I think

# Creation of menu (must be below labels so the label is above the selection which looks better)
menu_dropdown = ttk.Combobox(root, values = dropdown_choices, textvariable = store_user_input) #textvariable is from ttk
menu_dropdown.pack(anchor = W, padx = 10, pady = 5) #anchor defines position of widget in window I think. Uses compass directions or center.
menu_dropdown.bind("<<ComboboxSelected>>", CheckButton) #binds an event handler (Combo) to a specific event (CheckButton)

root.mainloop() #runs the GUI


