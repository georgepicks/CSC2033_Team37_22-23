# Team 37 Project: Leftovers
## Running The Application
### Setting Up Environment and Code
In order to run this program, it must be configured as a Flask server in PyCharm, to do this, follow these steps:
1. Download and install a Python interpreter (version 10 recommended), available here: https://www.python.org/downloads
2. Download and install PyCharm, available here: https://www.jetbrains.com/pycharm/download/
3. Clone this repository to PyCharm by clicking "Get From VCS" on the main menu and using this link: https://github.com/newcastleuniversity-computing/CSC2033_Team37_22-23.git
4. Click "File" in the top menu, then "Settings", in the new menu pop-up click "Project Interpreter" in the sub-menu of "Project: CSC2033_Team37_22-23"
5. From this menu, Click "Add Interpreter" followed by "Add Local Interpreter", PyCharm should auto-suggest the python interpreter you installed in step 1, if not, navigate to it in the file explorer pop-up
6. Click "Apply", exit the menu, click the drop-down menu in the top-right of the screen labelled "Open 'Edit Run/Debug configurations' dialog", followed by "Edit Configurations"
7. Click the "+" icon in the new menu, then select "Flask server", under the "Environment" label in the menu on the right, select your local python interpreter.
8. Click "Apply", exit the menu

The environment is now ready to run the application, although before it can be run successfully, dependencies must be installed.
### Installing Dependencies
This repository contains a file which is filled with the names of external packages it is dependent on, named 'requirements.txt'.
To install these dependencies enter this command in the PyCharm terminal (located in the bottom menu):

`pip install -r requirements.txt`

