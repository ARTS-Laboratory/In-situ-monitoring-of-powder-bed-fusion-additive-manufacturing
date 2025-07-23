import subprocess
import os

def run(cmd):
    try:
         completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    except:
         print('An error has occured')
    return completed

def clean(cleaner):
     cleaner = cleaner.replace(',','').replace("'","").replace("(","").replace(")","").replace('"','')
     return cleaner
     

mv_viewer_location = 'C:\\Users\\CBUREN\\Documents\\GitHub\\openeb\\build\\sdk\\modules\\stream\\cpp\\samples\\metavision_viewer'
os.chdir(mv_viewer_location)
print("New directory: ", os.getcwd())

print('What do you want to do? Enter 0-9\n0: End Program\n1: Live Stream Camera Feed\n2: Open RAW File\n3: Additional Options')
input_num = int(input())

while(input_num > 0):
        if(input_num == 1):
             PS_code = run('metavision_viewer.exe')
             print('Viewer opened. If you would like to end process enter 0 otherwise enter desired number.')
             input_num = int(input())

        if(input_num == 2):
             print('Path to .raw file: ')
             raw_path_unclean = input()
             raw_path_clean = clean(raw_path_unclean)
             raw_path = 'metavision_viewer.exe -o ' + raw_path_clean
             PS_code = run(raw_path)
             print(raw_path)
             print('\nRecording opened. If you would like to end process enter 0 otherwise enter desired number.')
             input_num = int(input())

        if(input_num == 3):
             PS_code = run('metavision_viewer.exe -h')
             print('Options opened. If you would like to end process enter 0 otherwise enter desired number.')
             input_num = int(input())
             
