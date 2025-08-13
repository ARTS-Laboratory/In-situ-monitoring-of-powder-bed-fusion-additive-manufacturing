print("CD into the Release folder\n\tEx: <openeb>/build/bin/Release")

print("Ensure that all the paths are absolute not relative")

print("First copy the path of the .exe file you want to use:")
old_exe = input()
new_exe = old_exe.replace('"','')

print("Next where is the .raw file located:")
old_raw = input()
new_raw = old_raw.replace('"','')

print("What do you want to name the excel file:")
excel = input() + ".csv"

print(new_exe, new_raw, excel)