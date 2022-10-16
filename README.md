# My-Golf-Stats
A little App I created, for keeping track of my latest golf results
This App features the input of a new golf game and its results. 

It is written in PYTHON and the framework KIVY. 
This App is my frist try to get in touch with coding mobile apps
You find here all the files, you need to compile the app by yourself with buildozer. 
If you are just interested in the .apk, you find it in the folder

Tipps, Tricks and Feature-Requets are highly welcome :)

# Content of files
- buildozer.spec
  - you will need that, if you want to compile the app with buildozer by yourself  
- myapp.kv
  - this is where you put all the styling information for the app
- course.json
  - a file to store all the information about the golf courses
- runde.json
  - this is the start .json for all the information about your last games
- main.py
  - the place, where the magic happens :D the .py has to have the name main, otherwise buildozer will not recognize the file

# Future Features/Bug-fixes
Here is a list of features, I would like to add to this app (or better, try to add)

- bug-fixes
  - the app still shows the first point in the graph at 0,0

- features
  - show data as a list
  - delete data
  - add/delete golf courses
  - iOS Version
  - add calculation of the handicap

# Tutorial for building your app
I can not give you a complete tutorial, as I am also a beginner in this topic.
But I found the tutorial of @avianmission (https://github.com/avionmission) really helpful
You can find it here:

https://avionmission.github.io/blog/convert-py-to-apk-using-python-and-buildozer/
