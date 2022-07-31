import rumps
import threading
from functions import *


def formatTitle(song, artist):
    song_edited=""
    artist_edited=""
    if(len(song)>14): song_edited = song[0:12]+'..'
    else: song_edited = song
    if(len(artist)>10): artist_edited = artist[0:8]+'..'
    else: artist_edited = artist
    return song_edited + " - " + artist_edited

class AwesomeStatusBarApp(rumps.App):
    current_song=["",""]
    
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__(name="Playful", title="Now Playing", icon="icons/spotify.png")
        def refresh_title():
            # print('Refreshing')
            try:
                track = getCurrentTrack()
                # print(track)
                # print(" and ")
                # print(self.current_song)
                if(track[0]!=self.current_song[0] or track[1]!=self.current_song[1]):
                    # print("copying")
                    self.current_song=track.copy()
                    self.title = formatTitle(track[0], track[1])
            except:
                pass
            threading.Timer(4.0, refresh_title).start()
        refresh_title()

    @rumps.clicked("Play / Pause")
    def toggle(self, _):
        if(getState()=="playing"):
            pause()
        else:
            play()

    @rumps.clicked("Next")
    def skip_next(self, _):
        next()
        self.refresh_title_once()

    @rumps.clicked("Previous")
    def skip_prev(self, _):
        previous()
        self.refresh_title_once()

    def refresh_title_once(self):
            # print('Refreshing')
            try:
                track = getCurrentTrack();
                self.current_song=track.copy()
                self.title = formatTitle(track[0], track[1])
            except:
                pass
    
if __name__ == "__main__":
    AwesomeStatusBarApp().run()
