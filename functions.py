import subprocess

def play():
    scpt = """
    tell application "Spotify"
        play
    end tell
    """
    subprocess.run(["osascript", "-e", scpt])

def pause():
    scpt = """
    tell application "Spotify"
        pause
    end tell
    """
    subprocess.run(["osascript", "-e", scpt])
    
def next():
    scpt = """
    tell application "Spotify"
        next track
    end tell
    """
    subprocess.run(["osascript", "-e", scpt])
    
def previous():
    scpt = """
    tell application "Spotify"
        previous track
    end tell
    """
    subprocess.run(["osascript", "-e", scpt])

def getState():
    scpt = """
    tell application "Spotify"
        player state
    end tell
    """
    result = subprocess.run(
        ["osascript", "-e", scpt],
        capture_output=True,
        encoding="utf-8",
    )
    info = list(map(str.strip, result.stdout.split(",")))
    return info[0]

def getCurrentTrack():
    scpt = """
    getCurrentlyPlayingTrack()
    on getCurrentlyPlayingTrack()
        tell application "Spotify"
            set currentSong to current track's name
            set currentArtist to current track's artist
            return {currentSong, currentArtist}
        end tell
    end getCurrentlyPlayingTrack
    """
    result = subprocess.run(
        ["osascript", "-e", scpt],
        capture_output=True,
        encoding="utf-8",
    )
    info = list(map(str.strip, result.stdout.split(",")))
    return info