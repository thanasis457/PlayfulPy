import subprocess

def play():
    subprocess.run(["osascript", 'compiledFunctions/play.scpt'])

def pause():
    subprocess.run(["osascript", 'compiledFunctions/pause.scpt'])
    
def next():
    subprocess.run(["osascript", 'compiledFunctions/next.scpt'])
    
def previous():
    subprocess.run(["osascript", 'compiledFunctions/previous.scpt'])

def getState():
    result = subprocess.run(
        ["osascript",'compiledFunctions/state.scpt'],
        capture_output=True,
        encoding="utf-8",
    )
    info = list(map(str.strip, result.stdout.split(",")))
    return info[0]

def getCurrentTrack():
    result = subprocess.run(
        ["osascript", 'compiledFunctions/currentTrack.scpt'],
        capture_output=True,
        encoding="utf-8",
    )
    info = list(map(str.strip, result.stdout.split(",")))
    return info