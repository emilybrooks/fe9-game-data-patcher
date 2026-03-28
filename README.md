A quick tool I made to modify FE8Data.bin in Fire Emblem: Path of Radiance

<img alt="Patcher window" src="img/patcher.jpg" width=25%>

There's also a viewer that displays the data in FE8Data.bin

<img alt="Game data viewer window" src="img/viewer.jpg" width= 40%>

## Setup
(Last tested with Python 3.14.3)
Download the repository

In the command line, navigate to the root directory

Create virtual environment
`python -m venv venv`

Install the dependencies  
`pip install -r requirements.txt`

Install setuptools  
`pip install setuptools`

Navigate to ./fe9LZ77module

Build the module  
`python3 setup.py install`

Launch with patcher.bat and viewer.bat
