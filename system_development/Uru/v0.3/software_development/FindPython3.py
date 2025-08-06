import site

list_location = (site.getsitepackages())
location = ' '.join(list_location)
print_location = location.replace('\\\\','\\')
print(print_location)

#Use the second one or the one that looks like an actual file path Ex: C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\site-packages

