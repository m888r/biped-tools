# To just read the torques from a past run on Windows:
1. replace torques.txt with new data
2. run `biped-tools-env/Scripts/activate.bat`
   1. This env is only configured for windows, and you don't need to run this file if you're fine with installing the packages in your OS instead of an isolated environment
3. do `pip install -r requirements.txt`
4. run the tool with `python -m main.py`, has to be python 3.xx