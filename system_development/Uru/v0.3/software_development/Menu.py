'''
By: Charlie Buren
Date: 8/21/2025


Goals:
    - Make an menu to allow for selection of different .exe's 
    - Will allow for faster testing and better user expierence 

ToDo:
    1) Finish Streaming
    2) Add more as needed

Doc:
    - tkinter: https://docs.python.org/3/library/tkinter.html
    - CSV new header: https://stackoverflow.com/questions/51463449/replace-csv-header-without-deleting-the-other-rows

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
import csv


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

# Check if an error with entering code into PS
def PS_Error_Checker_and_Runner(cmd, successful_code_message): # runs the previous def using cmd code
    CodeRun = run_cmd(cmd)
    if CodeRun is None:
        messagebox.showerror("Error", "Failed to run command.")
        return False
    elif CodeRun.returncode != 0:
        messagebox.showerror("Error", f"Command failed:\n{CodeRun.stderr}")
        return False
    else:
        messagebox.showinfo("Success", successful_code_message)
        return True


# Cleans up the generated lines of code to ensure no errors occur
def clean(cleaner):
     cleaner = cleaner.replace(',','').replace("'","").replace("(","").replace(")","").replace('"','')
     return cleaner

# Replaces the old csv header with a new one
def csv_cleaner(csv_path, csv_output):
    header = ["X", "Y", "Output", "Value"]
    with open(csv_path, 'r') as fp:
        reader = csv.DictReader(fp, fieldnames=header)
        
        # use newline='' to avoid adding new CR at end of line
        with open(csv_output, 'w', newline='') as fh: 
            writer = csv.DictWriter(fh, fieldnames=reader.fieldnames)
            writer.writeheader()
            header_mapping = next(reader, None)
            writer.writerows(reader)
    return

# File selection
def OpenFile():
    # askopenfile allows user to pick file and returns the opened file in read only
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

# Asks the user where the .exe's are located and saves the location
def exe_folder_location():
    # askdirectory allows user to select a directory of exe loctions 
    global exe_folder_path # allows for variable to pulled outside of def
    exe_folder_path = filedialog.askdirectory(title = "Loction of .exe's"
                                              )
    
    # for testing
    if exe_folder_path:
        store_user_input_exeFolderLocation.set(exe_folder_path)
        folder_exe_label.config(text=f"Folder: {exe_folder_path}") # Show exe folder that was selected
        # messagebox.showinfo("Folder selcted", f"Path: {exe_folder_path}") #Use for testing
        return exe_folder_path
    else:
        messagebox.showerror("There was an error try again")
    return

# Check if exe has been selected
def check_exe_selection():
    exe_folder = globals().get("exe_folder_path", None)
    if not exe_folder:
        messagebox.showerror("Missing Folder", "Please select the .exe folder location before continuing.")
        return False
    return True

    
# Popup selection
def popup_options(title_selection_window, question_ask_str):
    # asks a yes or no question for the user to answer
    popup_ask = messagebox.askyesno(title = title_selection_window, # allows us to change the name of the title
                                       message = question_ask_str, # allows us to change the question that is being asked
                                    )
    # Don't store answer in here cause it will be hard to code at least it was for me
    return popup_ask


# --- Option defs ---
# Playback raw file only
def raw_file_playback():
    raw_playback_name = "metavision_viewer.exe" # exe name
    mv_raw_playback_path = os.path.join(exe_folder_path, raw_playback_name) # joins path of exe and the exe into one string
    print(mv_raw_playback_path)

    # Select a file
    file_path = OpenFile()
        
    # Ensure that file has been selected. If no file has been selected then it runs again.
    try:
        file_path
    except:
        messagebox.showerror("File Selection Error. Try again.")
        return
        
    #ensure that .csv was selected
    if file_path.lower().endswith(".raw"):
        cmd = f'& "{mv_raw_playback_path}" -i "{file_path}"'
        print(cmd) #testing

        #Run the PS code w/ error messages
        PS_Error_Checker_and_Runner(cmd, "Playback Successful!")
        return
        
    else:
        messagebox.showerror("Please Select a .raw file")
        return

    return

# Playback recordings
def mv_viewer_playback():
    #adds an error incase no exe folder has been selected. Doesn't crash the program now
    if not check_exe_selection(): 
        return 
  
    # asks the user if they want to read from a csv or raw file
    csv_or_raw_popup = popup_options(".raw or .csv?", # title of popup 
                                     "Are you trying to playback recording from a .csv or .raw file? \nYes: Opens .csv file \nNo: Opens .raw file") # question that is asked

    #if statment for yes (.csv) Completed
    if csv_or_raw_popup: # if yes was entered
        csv_playback_name = "metavision_csv_viewer.exe" # exe name
        mv_csv_playback_path = os.path.join(exe_folder_path, csv_playback_name) # joins path of exe and the exe into one string
        print(mv_csv_playback_path)

        # Select a file
        file_path = OpenFile()
        
        # Ensure that file has been selected. If no file has been selected then it runs again.
        try:
            file_path
        except:
            messagebox.showerror("File Selection Error. Try again.")
            return
        
        #ensure that .csv was selected
        if file_path.lower().endswith(".csv"):
            cmd = f'& "{mv_csv_playback_path}" -i "{file_path}"'
            print(cmd) #testing

            #Run the PS code w/ error messages
            PS_Error_Checker_and_Runner(cmd, "Playback Successful!")
            return
        else:
            messagebox.showerror("Please Select a .csv file")
            return
    else:
        raw_file_playback()
    return

# Convert .raw file to a .csv in the same location as the raw file
# Works don't change unless needed
def raw_to_csv():
     #adds an error incase no exe folder has been selected. Doesn't crash the program now
     if not check_exe_selection(): 
         return
     
     evt3_converter_name = "metavision_evt3_raw_file_decoder.exe" # exe name
     mv_evt3_conv_path = os.path.join(exe_folder_path, evt3_converter_name) # joins path of exe and the exe into one string
     print(mv_evt3_conv_path)

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
         cmd = [mv_evt3_conv_path, file_path, created_csv] # combines the strings to create the code
         print(cmd) #testing

         # Run the PS code. This gives the errors or says if it works
         PS_Error_Checker_and_Runner(cmd, "Conversion Successful!")

         # Adds ML to the csv name 
         csv_new_output = created_csv.replace('.csv', '_ML.csv')
         
         # Cleans the csv and adds the right header
         csv_cleaner(created_csv, csv_new_output)

         # Deletes the file w/o ML in the name
         os.remove(created_csv)    

     else:
         messagebox.showerror("Please Select a .raw file")

# Trim a recording 
def mv_trimer():
    #adds an error incase no exe folder has been selected. Doesn't crash the program now
    if not check_exe_selection(): 
        return 

    # Ask if user needs to view recording
    view_playback_popup = popup_options("Playback Popup", # title of popup window
                                         "Do you need to view the recording playback?") # question that is asked
    
    global view_playback_trimmer_yes_selected # allows for boolean to called anywhere. 
    
    # if yes for view_playback_popup is selected 
    if view_playback_popup:
        view_playback_trimmer_yes_selected = True
    else:
        view_playback_trimmer_yes_selected = False

    # Run the trimmer 
    trimer_exe_name = "metavision_file_cutter.exe" # exe name
    mv_trimmer_path = os.path.join(exe_folder_path, trimer_exe_name) # joins path of exe and the exe into one string
    print(mv_trimmer_path)

    # Select a file
    file_path = OpenFile()
        
    # Ensure that file has been selected. If no file has been selected then it runs again.
    try:
        file_path
    except:
        messagebox.showerror("File Selection Error. Try again.")
        return
        
    #ensure that .csv was selected
    if file_path.lower().endswith(".raw"):
        cmd = f'& "{mv_trimmer_path}" -i "{file_path}"'
        print(cmd) #testing

        # Run the PS code w/ error messages
        PS_Error_Checker_and_Runner(cmd, "Trimmer Opened!")
        return
    else:
        messagebox.showerror("Please Select a .raw file")
        
    # checks if file is raw file and returns error if not


    return

# record
def mv_record():
    #adds an error incase no exe folder has been selected. Doesn't crash the program now
    if not check_exe_selection(): 
         return
     
    mv_streamer_name = "metavision_viewer.exe" # exe name
    mv_streamer_path = os.path.join(exe_folder_path, mv_streamer_name) # joins path of exe and the exe into one string
    print(mv_streamer_path)

    output_folder_path = filedialog.askdirectory(title = "What is the output folder?")

    # for testing
    if not output_folder_path:
        messagebox.showerror("There was an error try again")

    store_user_input_outputFolderLocation.set(output_folder_path)

    # --- Open Instructions ---
    # Get the absolute path of the current script
    script_path = os.path.abspath(__file__)
    
    # Get the directory containing the script
    script_directory = os.path.dirname(script_path)

    instructions_file_location = f'{script_directory}\Recording_Instructions.txt'

    # --- Load Settings ---
    load_settings_popup = popup_options("Settings", # title of popup 
                                         "Do you want to load any settings?" # question that is asked
                                        )
     
    # JSON loading
    if load_settings_popup:
        # Select a .json file to load the settings
        file_path_json = OpenFile()
         
        # Ensure that file has been selected. If no file has been selected then it runs again.
        try:
            file_path_json
        except:
            messagebox.showerror("File Selection Error. Try again.")
            return
        
        #ensure that json was selected
        if file_path_json.lower().endswith(".json"):
            cmd = f'& "{mv_streamer_path}" -j "{file_path_json}" -o "{output_folder_path}"'
            os.startfile(instructions_file_location)
            print(cmd) #testing

            #Run the PS code w/ error messages
            PS_Error_Checker_and_Runner(cmd, "Playback Successful!")
            return
        else:
            messagebox.showerror("Please Select a .json file")
            return
    
    #No settings
    else:
        cmd = f'& "{mv_streamer_name}" -o "{output_folder_path}"'
        os.startfile(instructions_file_location)
        print(cmd) #testing

        #Run the PS code w/ error messages
        PS_Error_Checker_and_Runner(cmd, "Playback Successful!")
        return
     

# --- Check Button (Put Options above it) ---
# Catch the Check Button Event
def CheckButton(event):
    exe_selection = store_user_input_optionSelection.get() #.get() returns the value of the item with the specified key.
    messagebox.showinfo("Selection Menu", "You have selected the option: " + str(exe_selection)) #idk what it does but everyone had it like this

    #if statements
    if exe_selection == 'Stream from Camera':
        mv_record()
    elif exe_selection == 'View recordings':
        mv_viewer_playback()
    elif exe_selection == 'Trim a recording':
        mv_trimer()
    elif exe_selection == 'Convert .raw file to .csv':
        raw_to_csv()
    # Error Line for errors or not completed options
    else: 
        messagebox.showinfo("Selection Menu", "Invalid selection:" + str(exe_selection))


## --- Start Menu ---
# root setup
root = Tk() #root is toplevel menu. Root adds a seperate window that is the background I think. Its like opening a new tab I believe 
root.title("Uru Menu") #Adds a window title
resulution = '350x300' # size of window
root.geometry(resulution)

# list of all choices in the drop down menu
dropdown_choices = ['Stream from Camera', 
                    'View recordings', 
                    'Trim a recording',
                    'Convert .raw file to .csv'] 

# String Stores user selection
store_user_input_optionSelection = StringVar()
store_user_input_exeFolderLocation = StringVar()
store_user_input_outputFolderLocation = StringVar()

# Creation of menu labels
menu_label = Label(root, text = 'Select an .exe')
menu_label.pack(anchor = W, padx = 10, pady = 10) #padx or pady desinates the exteral padding on each side. That means how big will it be I think

# Creation of menu (must be below labels so the label is above the selection which looks better)
menu_dropdown = ttk.Combobox(root, values = dropdown_choices, textvariable = store_user_input_optionSelection) #textvariable is from ttk
menu_dropdown.pack(anchor = W, padx = 15, pady = 5) #anchor defines position of widget in window I think. Uses compass directions or center.
menu_dropdown.bind("<<ComboboxSelected>>", CheckButton) #binds an event handler (Combo) to a specific event (CheckButton)

# Creation of .exe folder location selection
folder_exe_selection = Button(root, text = "Select .exe folder loctaion: ", command = exe_folder_location)
folder_exe_selection.pack(anchor = W, padx = 15, pady = 5)

# Label for exe folder
folder_exe_label = Label(root, text="No folder selected")
folder_exe_label.pack(anchor=W, padx=15, pady=(0, 10))  # Smaller padding for tight layout


print(store_user_input_exeFolderLocation)

root.mainloop() #runs the GUI


