------------------------------------------------------------------------------------------------------------------------------------------

Created by: Charlie Buren
Date of last change: 8/08/2025

Notes: 
	- If you have any questions or concerns please email me at: cburen@email.sc.edu
	- If you don't want to do these steps and just want the .exe's then look in the metavision_executables folder on GitHub. Just make 
	  make sure to copy them to a new folder so you don't overwrite them on accident. 
------------------------------------------------------------------------------------------------------------------------------------------

Using GUI
 1) Copy metavision_executables folder into a new folder not in the github
	- Ensures that any errrors don't change the exe's
 2) When GUI asks for exe folder select that new folder that you just created
 3) Select the exe folder first before doing anything else

------------------------------------------------------------------------------------------------------------------------------------------

Video Exporting

1. Using Metavision Studio
	1) Open the recording that you desire to export to video
	2) Trim the recording using the options on the toolbar
	3) If desired change the frame rate of video
		3.1) 250 for regular slowed down video
			- If slower is desired use 300 or 500. 
		3.2) 1 for real time speed

2. Using GUI
	- Not Done Yet

------------------------------------------------------------------------------------------------------------------------------------------

Installation guide

1. Prerequisites
	1.1 Go to https://docs.prophesee.ai/4.6.2/installation/windows_openeb.html#chapter-installation-windows-openeb
	1.2 Install
		1) Git: https://git-scm.com/downloads/win
		2) CMake
			2.1) Download newest version of CMake: https://cmake.org/download/
				1) Download the x64 Installer
					- Downloading zip is recommended for the ReadMe
				2) Run the installer
				3) Ensure that CMake is added to your PATHS
				4) If not then add it
					- This done by finding the install location and copying the location into a new PATH
					- ex: C:\Program Files\CMake\bin
			2.2) Download MSYS2: https://www.msys2.org/#installation
				- Once the exe is downloaded run it and enter $ pacman -S --needed git base-devel mingw-w64-x86_64-					  gcc
				-Then enter y when it asks if you want install
2. Clone the repos:
	a) openb: https://github.com/prophesee-ai/openeb
		-The install location will be referred to <openb>
			-Ex: C:\Users\CBUREN\Documents\GitHub\openeb
	b) vcpkg: https://github.com/microsoft/vcpkg
		-The install location will be referred to <vcpkg>
			-Ex: C:\Users\CBUREN\Documents\GitHub\vcpkg
	c) dirent: https://github.com/tronkko/dirent
		-The install location will be referred to <dirent>
			-Ex: C:\Users\CBUREN\Documents\GitHub\dirent

3. Set up vcpkg
	3.1 Open Powershell and
		1) cd <vcpkg>
		2) .\bootstrap-vcpkg.bat
	    	   .\vcpkg update
		3) git pull
		4) .\vcpkg install hdf5:x64-windows
	3.2 Then go to C:\<openb>\utils\windows and copy the vcpkg-openeb.json into <vcpkg> and change the name to vcpkg.json 
	    	- Open the file and copy the COPYTHIS.txt into vcpkg.json
	3.3 Using PS enter
		- .\vcpkg install boost-thread:x64-windows
	
	3.3 If failed then try the following
	  -Note: The error logs can be found in <vcpkg>\buildtrees. Then go to the file that corresponds to the error.
	  -If you do any of these steps remove vcpkg.json and then once done with these steps add it back
		1) .\vcpkg remove boost-thread --recurse
		2) .\vcpkg remove boost --recurse
		3) Remove-Item -Recurse -Force .\buildtrees
		4) Remove-Item -Recurse -Force .\packages
		5) Remove-Item -Recurse -Force .\installed
		6) Then use update and git pull
		7) If these steps didn't work then find error that what was listed and go to the error logs

4. Download and setup Python
	4.1 Should be 3.12: https://www.python.org/downloads/release/python-3120/
		- Add the directories to you paths. 
	4.2 Virtual Environment
		1) Launch Visual Studio and open the terminal
		2) In the terminal enter: python -m venv C:\tmp\prophesee\py3venv --system-site-package
		3) Enter in terminal: pip install "pybind11[global]"
		4) Enter in terminal: set PYTHONNOUSERSITE=true
		5) Enter in terminal: C:\tmp\prophesee\py3venv\Scripts\python -m pip install pip --upgrade
C:\tmp\prophesee\py3venv\Scripts\python -m pip install -r <openeb>\utils\python\requirements_openeb.txt

5. Compilation using CMake
-NOTE: ITS OK IF YOU CAN'T GET THIS DONE. JUST SKIP TO THE NEXT SECTION
	5.1 Compiling
		1) In <openeb> open a cmd and enter: mkdir build
		2) Enter: cd build
		3) In a new PS enter
			3.1) <vcpkg>\vcpkg.exe install libtiff:x64-windows
			3.2) <vcpkg>\vcpkg.exe install boost-program-options:x64-windows boost-timer:x64-windows boost-chrono:x64-windows boost-thread:x64-windows
			3.3) <vcpkg>\vcpkg.exe install pybind11:x64-windows
			3.4) <vcpkg>\vcpkg.exe install tiff:x64-windows
		4) CD back into <openeb>\build & enter: cmake .. -A x64 -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=<OPENEB_SRC_DIR>\cmake\toolchains\vcpkg.cmake -DVCPKG_DIRECTORY=<VCPKG_SRC_DIR> -DBUILD_TESTING=OFF
			- Note: Ensure to change the paths in command
		5) Enter: cmake --build . --config Release --parallel 4

	5.2 Deploying
		1) Run CMD as admin and cd into <openeb>\build
		2) Enter: cmake .. -A x64 -DCMAKE_TOOLCHAIN_FILE=<OPENEB_SRC_DIR>\cmake\toolchains\vcpkg.cmake -DVCPKG_DIRECTORY=<VCPKG_SRC_DIR> -DCMAKE_INSTALL_PREFIX=<OPENEB_INSTALL_DIR> -DPYTHON3_SITE_PACKAGES=<PYTHON3_PACKAGES_INSTALL_DIR> -DBUILD_TESTING=OFF
			- Notes:
				- Ensure to change the paths in command
				- <PYTHON3_PACKAGES_INSTALL_DIR> can be found by running the python script: FindPython3
		3) Environment variables
		  -NOTE: If the variable exists add a semicolon (;) and then the path
			1) <openeb>\bin to PATH
			2) C:\Program Files\Prophesee\lib\metavision\hal\plugins as MV_HAL_PLUGIN_PATH
			3) <openeb>\lib\hdf5\plugin to HDF5_PLUGIN_PATH
			4) <PYTHON3_PACKAGES_INSTALL_DIR> to PYTHONPATH 
	

6. Compilation using Visual Studio 
-Note: If failed to complie using CMake delete the build folder
-Note: If you are getting errors cd into <vcpkg> and enter: git pull & git update
	6.1 Open CMD and enter:
		1) cd <openeb>
		2) mkdir build
		3) cd build
		4) cmake .. -G "Visual Studio 17 2022" -A x64 -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=C:<openeb>\cmake\toolchains\vcpkg.cmake -DVCPKG_DIRECTORY=<vcpkg> -DBUILD_TESTING=OFF 
			Error: If you get CMake Error at build/vcpkg_installed/x64-windows/share/hdf5/hdf5-targets.cmake:42 (message):
  			       Some (but not all) targets in this export set were already defined.
			       Targets Defined: hdf5::h5diff
			Fix: cd into just <openeb> and enter findstr /s /n /i "find_package(HDF5" *.txt *.cmake and find where the error is
				

			Note: -DCMAKE_TOOLCHAIN_FILE needs to be an absolute path
			      -If you get the error "CMake Error at cmake/custom_functions/python3.cmake:178 (find_package):
  	    		       By not providing "Findpybind11.cmake" in CMAKE_MODULE_PATH this project has
  	 		       asked CMake to find a package configuration file provided by "pybind11",
  	    		       but CMake did not find one."  
				!!!!!-Then you should cd <vcpkg> then enter: .\vcpkg install pybind11:x64-windows
			      -If you get the error "CMake Error at C:/Program Files/Prophesee/third_party/share/hdf5/hdf5-config.cmake:25 			       (message):
  	    		       File or directory C:/Program Files/Prophesee/third_party/tools/hdf5
  	    		       referenced by variable HDF5_TOOLS_DIR does not exist !"
				!!!!! Then cd <vcpkg> and enter: .\vcpkg install hdf5:x64-windows

	6.2 Open metavision.sln in Visual Studio
		1) Mine was located at: C:\Users\CBUREN\Documents\GitHub\openeb\build
		2) At the top near the green play button at the top select RELEASE from the drop down menu and hit the play button. 
		3) Go to Solution Explorer right click ALL_BUILD and hit build and then do the same for INSTALL
	6.3 Change environment variables
		1) Append C:\Program Files\Prophesee\bin to PATH
		2) append C:\Program Files\Prophesee\lib\metavision\hal\plugins to MV_HAL_PLUGIN_PATH
		3) append C:\Program Files\Prophesee\lib\hdf5\plugin to HDF5_PLUGIN_PATH

7. Drivers
	1) Install: wdi-simple.exe from: https://kdrive.infomaniak.com/app/share/975517/cb164518-e68f-49fd-a6a1-eea693783bd2/preview/unknown/90270
	2) Run CMD as admin and cd into downloads folder1
	3) Enter: wdi-simple.exe -n "EVK" -m "Prophesee" -v 0x04b4 -p 0x00f4
wdi-simple.exe -n "EVK" -m "Prophesee" -v 0x04b4 -p 0x00f5
wdi-simple.exe -n "EVK" -m "Prophesee" -v 0x04b4 -p 0x00f3

8. Running
	1) Add new folder in <openeb> called datasets
	2) cd C:\School\Research\GitHub\openeb\build
	3) cmake .. -A x64 -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=C:\School\Research\GitHub\openeb\cmake\toolchains\vcpkg.cmake -DVCPKG_DIRECTORY=C:\School\Research\GitHub\vcpkg -DBUILD_TESTING=OFF
	4) cmake --build . --config Release --parallel 4

------------------------------------------------------------------------------------------------------------------------------------------

Issues:
  - Leave any issues that you may encounter here
	1) Problem 1
	   - Fix 1

	

