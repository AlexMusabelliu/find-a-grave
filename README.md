# Installation
First, you need python: https://www.python.org/downloads/

You then need to install 3 dependencies, listed in requirements.txt

To get those, go to the CMD in windows (search + "CMD") (if you're on MAC and don't know how to use the command line there, I'm sorry, I don't know either)

then type the following:
```
cd [path name of where you installed this, e.g. C:\User\Downloads\find-a-grave-main]
pip install requirements.txt
```
# Usage
run it using the `run.bat` in the folder

when asked for the starting position, if you don't know any just press enter or type 0 and press enter. 

if you've run the program before, a log is created at `log[date].txt`, where you can find the point you left off at: type that in at this point to begin from there and append to the output.

# Results
ouput is located in a folder that is created once you run this program, `output/confirmed_dead.csv`. In the CSV are the people who had returned matches from searching the person's name on findagrave.com.

if you run the program again, it will append to this file, even if you run it from the very start again, so if you want to replace this file **DELETE IT FIRST** then run the program again.

# Notice
this is a custom version of the main branch and operates under the assumption that the list you're giving it is confirmed as voting. if that's not the case, use the main branch, not this one.
