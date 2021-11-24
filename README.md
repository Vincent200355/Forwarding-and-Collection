
# Forwarding-and-Collection

## Getting Started

These steps will give you an instruction on how to locally deploy the project. To get a local copy clone the repository into a directory of your choice.

### Prerequisites

This project uses [Python 3.9.7](https://www.python.org/downloads/release/python-397/)
For the installation process make sure to activate `Add Python 3.X to PATH` 
![alt text](http://url/to/img.png)

After installing python, make sure to verify that the correct version is installed. Using `py --version` should result in the following output `Python 3.9.7`

Using an already installed version of python the command could also be `python` instead of `py`. **In this case use `python` for all of the following commands.**
### Installation
Head into the cloned directory folder which sould look like the following:
<pre>
Forwarding-and-Collection/
├── .git/
│   └── ...
├── .gitignore
├── README.md
└── requirements.txt
</pre>

Navigate into Forwarding-and-Collection and run the following commands in order to
1. Create the environment:
	On Windows
	```
	py -m venv env
	```
2. Activate the environment
	On Windows
	```
	env\Scripts\activate.bat
	```
	On Unix or MacOS
	```
	source env/bin/activate
	```
	After successfully activating the environment your terminal line should begin with (env)
3. Install the required packages using `requirements.txt`
	After activating the environment make surre to navigate to the repositories top directory which is `Forwarding-and-Collection`.
	```
	py -m pip install -r requirements.txt
	```
### Usage
Everytime you want to execute code inside the environment you need to activate it by following `Step 2. of Installation`

### Adding requirements to the repository
In case you are using [pip](https://pypi.org/project/pip/) packages for your code, make sure to add them to `requirements.txt` so that other group members can easily install the right versions of them without needing to manually install each.

1. Activate the environment
2. Navigate to the top level of the repository folder, which is `Forwarding-and-Collection`
3. Run
	```
	pip freeze > requirements.txt
	```