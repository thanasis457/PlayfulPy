# <img src="icons/app.icns" align="left" width="114"/> Playful-Py for Spotify

A simple, clean, MacOS application that displays the current song on the Menu Bar. Works only with Spotify.    


This project is a complete rewrite of [Playful](https://github.com/thanasis457/Playful) with a focus on efficiency and low resource use, written in Python.

## Screenshots
![](https://i.imgur.com/ZmtXkHh.png)
![Imgur](https://i.imgur.com/kqLtBuR.png)

## Installing

The easiest way to get running is to head to Releases and download the package for your platform.

### For reference:

MacOS Intel (x64): PlayfulPy-darwin-x64-[version].zip  
MacOS Apple Silicon (arm64): PlayfulPy-darwin-arm64-[version].zip  

## Installing from source

1. `git clone https://github.com/thanasis457/PlayfulPy`

2. `cd PlayfulPy`

3. `pip install -r requirements.txt`

4. `python PlayfulPy.py` to run

Done!  
The app should now be running.

### Packaging the application
To make a distributable version of the app yourself you will need to follow a couple more steps. We will be using py2app.

From inside the project folder run:
1. `pip install py2app`
2. `python setup.py py2app`

There should now be two folders in the project folder named `build` and `dist`. Inside `dist` you will find your distributable.

## Extra information

### Caution

Due to a change in the `collections` interface in Python 3.10, any version since 3.10 is not able to run `rumps`(project dependency) properly,
so make sure you run the project on any version of Python earlier than that.

### What about Playful?
Playful was my first attempt to create a Menu Bar Spotify player. It runs on Electron/NodeJS and handles all communication with Spotify through their API.
Electron is essentially a whole Chromium instance, meaning it has a lot of overhead processing, let alone memory and file size. Plus, accessing the API
constantly and reliably can be finicky at times.

PlayfulPy aims to eliminate both these issues by using plain Python scripts, which are far more efficient, and accessing Spotify playback controls
and data through Applescripts. Everything is being done locally and without complicated processes.
In addition, PlayfulPy refreshes the current song title in a different process (using `threading`) so as to not block the main process, making it ever so
slightly more efficient.

### Notes

- As already stated, use Python versions earlier than 3.10 or try to figure out fixes for the issues and let me know of any solutions.
- The packaged releases are fully standalone apps. They do not require Python to be installed on the target machine.
- The App icons are not mine. They are provided by Icons8 and can be found [here](https://icons8.com/icon/116726/spotify)
- Support for Linux/Windows: Accessing Spotify playback status is a different challenge for every platform. Should I port the app, there would be
a whole lot more problems to solve. In addition, neither platform provides an easy way to access the system's menu bar/tray and set text (to show the current song).
They only allow the showing of icons. Thus, supporting these platforms seems highly unlikely (at least for now).
