# Study_FastAPI

The elaboration of this test serves to assess the abilities and proficiency 
of the applicants in using the tool.

## Prerequisite

* You can obtain the latest version of Python (Python 3.11.5) at: https://www.python.org/downloads/
* Any integrated development environment (IDE) such as Visual Studio Code or PyCharm.
* GIT will also be required for version control.

## Installation

* Open a terminal on your computer.
* Navigate to the directory where you want to clone the repository using the cd command. For example:
cd ~/Documents ... Change the path to your preferred directory
* Clone the repository using the git clone command followed by the repository's URL: https://github.com/StevenGoez/Prueba_Tecnica_FastAPI.git
* Once the repository is cloned, navigate to the cloned project directory: cd yourproject
* Create a virtual environment for the project (optional but recommended). You can use venv or virtualenv:
* Then, activate the virtual environment:
    On Unix/macOS systems: source venv/bin/activate
    On Windows (PowerShell): .\venv\Scripts\Activate.ps1
    On Windows (CMD): .\venv\Scripts\activate

* Install the project dependencies using pip and the requirements.txt file: pip install -r requirements.txt
* Run the FastAPI application using uvicorn. Make sure your FastAPI application is in an accessible Python file (e.g., main.py): uvicorn app.main:app --reload
Replace "main" with the name of your main file if it's different.

## Tests

You can use the pytest command in the terminal or select each test individually and check the results. I prefer the latter option for my preference.

## Usage

Once you run the project using the uvicorn command, it will open on the local host. Please navigate to http://127.0.0.1:8000/docs to see all available routes. There are 5 available routes:

1. Get Users and Get Addresses: These routes allow you to retrieve users and addresses stored. Since this exercise does not use a database, the data is stored in lists during execution. If the lists contain users and/or addresses, these requests will show you the stored information.

2. Create User and Create Address: These routes are used to create users and addresses with a mandatory request body, which is in JSON format and does not allow empty or default values. These routes are used to store information within lists, and the relationship between users and addresses is based on the email. You cannot create an address without a valid user, as the email of the user is required to create an address.

3. Filter Users by Country: This route requires providing a country as a parameter, and it will search for users with that country in their address.

## Contact

- Steven Goez: steven.goez@gmail.com
- WhatsApp: +57 3004947487
