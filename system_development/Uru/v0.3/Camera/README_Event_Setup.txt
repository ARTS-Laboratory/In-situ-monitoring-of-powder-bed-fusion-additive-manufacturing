Installation Guide. Since the files to be able to control the event camera are over 5ish GB I can't to upload them to the GitHub. 
I followed the guide so you can ignore this file and just look at the website, but I added more onto it so it should help with simplicity. If you have any questions you can contact me at cburen@email.sc.edu 

Note: CMD/PS will be interchangeably it doesn't matter which one you use. If you are using CMD then remove the .\ from the beginning of the input, and if you're using powershell you might have to add it

1. Follow the guide: https://docs.prophesee.ai/stable/installation/windows_openeb.html#chapter-installation-windows-openeb
	1.1 Install Metavision from https://docs.prophesee.ai/stable/installation/index.html
	1.2 Install git
	1.3 Install CMake 3.26 (more recent versions might not be compatible)
	1.4 Install Microsoft Visual C++ compiler (MSVC, 64-bit version) included in Visual Studio 2022 - Fall 2023 LTSC (version 17.8). 	    If you install the Build Tools only, make sure Windows 10 SDK is checked, and add English Language Pack.
	1.5 Enable long paths by 
		1. Hit the Windows key, type gpedit.msc and press Enter
		2. Navigate to Local Computer Policy > Computer Configuration > Administrative Templates > System > Filesystem
		3. Double-click the “Enable Win32 long paths” option, select the “Enabled” option and click “OK”
	1.6 Install ffmpeg and add the directory to you paths. 

2. Clone the repos:
	a) openb: https://github.com/prophesee-ai/openeb
		-The install location will be referred to <openb>
			-Ex: C:\Users\CBUREN\Documents\GitHub\vcpkg
	b) https://github.com/microsoft/vcpkg
		-The install location will be referred to <vcpkg>
			-Ex: C:\Users\CBUREN\Documents\GitHub\openeb

3. Using powershell do the following
	3.1 cd <vcpkg>
	3.2 .\bootstrap-vcpkg.bat
	    .\vcpkg update
	3.3 git pull
	3.4 .\vcpkg install boost-thread:x64-windows
	

4. Then go to C:\<openb>\utils\windows and copy the vcpkg-openeb.json into <vcpkg> and change the name to vcpkg.json
	4.1 Open the file and copy the COPYTHIS.txt into it

5. Then using PowerShell again in the cd vcpkg enter ".\vcpkg install --triplet x64-windows"

6. If failed then do the following
	6.1 .\vcpkg remove boost-thread --recurse
	6.2 .\vcpkg remove boost --recurse
	6.3 Remove-Item -Recurse -Force .\buildtrees
	6.4 Remove-Item -Recurse -Force .\packages
	6.5 Remove-Item -Recurse -Force .\installed
	6.6 Then use update and git pull
	6.7 If these steps didn't work then find error that what was listed and go to the error logs 
		-The error logs can be found in <vcpkg>\buildtrees. Then go to the file that corresponds to the error. 

7. Download and setup Python
	7.1 Must be 3.12
		7.1.1 Added the directories to you paths. 
	7.2 Virtual Environment
		7.2.1 Launch Visual Studio and open the terminal
		7.2.2 In the terminal enter: python -m venv C:\tmp\prophesee\py3venv --system-site-package
		7.2.3 Enter in terminal: pip install "pybind11[global]"
		7.2.4 Enter in terminal: set PYTHONNOUSERSITE=true
		7.2.5 Enter in terminal: C:\tmp\prophesee\py3venv\Scripts\python -m pip install pip --upgrade
C:\tmp\prophesee\py3venv\Scripts\python -m pip install -r <openeb>\utils\python\requirements_openeb.txt
			
8. Compilation using Visual Studio 
Note if you want you can use CMake for the compilation, but I didn't test this
	8.1 Open CMD and enter:
		8.1.1 cd <openeb>
		8.1.2 mkdir build
		8.1.3 cd build
		8.1.4 cmake .. -G "Visual Studio 17 2022" -A x64 -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=C:<openeb>\cmake\toolchains\vcpkg.cmake -DVCPKG_DIRECTORY=<vcpkg> -DBUILD_TESTING=OFF 

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

	8.2 Open metavision.sln in Visual Studio
		8.2.1 Mine was located at: C:\Users\CBUREN\Documents\GitHub\openeb\build
		8.2.2 At the top near the green play button at the top select release from the drop down menu and hit the play button. 
		8.2.3 Go to Solution Explorer right click ALL_BUILD and hit build and then do the same for INSTALL
	8.3 You can either do option 1 or 2. I did option 2 so I suggest that you do that
		8.3.1 Append C:\Program Files\Prophesee\bin to PATH
		8.3.2 append C:\Program Files\Prophesee\lib\metavision\hal\plugins to MV_HAL_PLUGIN_PATH
		8.3.3 append C:\Program Files\Prophesee\lib\hdf5\plugin to HDF5_PLUGIN_PATH

9. Camera Plugins
	9.1 Download wdi-simple.exe from https://kdrive.infomaniak.com/app/share/975517/cb164518-e68f-49fd-a6a1-eea693783bd2/preview/unknown/90270

	9.2 As an administer launch CMD then enter: "wdi-simple.exe -n "EVK" -m "Prophesee" -v 0x04b4 -p 0x00f4
wdi-simple.exe -n "EVK" -m "Prophesee" -v 0x04b4 -p 0x00f5
wdi-simple.exe -n "EVK" -m "Prophesee" -v 0x04b4 -p 0x00f3"

10. Run Tests
	10.1 Download OpenEB test data (it is 1.5gb)
	10.2 If needed make a new folder in <openeb> called datasets
		10.2.1 In datasets make a new folder called openeb. You'll place the raw files in this folder.
	10.3 cd <openeb>/build
	10.4 cmake .. -A x64 -DCMAKE_TOOLCHAIN_FILE=<openeb>\cmake\toolchains\vcpkg.cmake -DVCPKG_DIRECTORY=<vcpkg> -DBUILD_TESTING=ON 
		Note: I would make both paths absolute paths
		10.4.1 If you get the error about pytest then you need to open a new PS and enter 
			C:\tmp\prophesee\py3venv\Scripts\activate
			python -m pip install pytest

		10.4.2 If you get error about gtest remove vcpkg.json from <vcpkg> and then cd <vcpkg> and enter .\vcpkg install gtest --triplet x64-windows
	
	10.5 Then compile by entering into PS: cmake --build . --config Release --parallel 4
	10.6 After you do that you can now use EVT_PS
		10.6.1 Can work with any .exe in <openeb>\bin\Release, but is designed for the evt ones. 

11. Getting the raw files
	11.1 cd into the folder that you want to put the .csv into
	11.2 Use Event_PS to get the powershell code and then copy the code into PS

		





	
	
