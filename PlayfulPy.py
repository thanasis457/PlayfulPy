import rumps
import threading
from functions import *
import configparser

config = configparser.ConfigParser()
config.read('PlayfulPy.ini')

def formatTitle(song, artist, length):
    if(length=='Long'):    
        song_edited=song
        artist_edited=artist
        if(len(song)+len(artist)>40):
            if(len(artist)>16 and len(song)>24):
                artist_edited = artist[0:14]+'..'
                song_edited=song[0:22]+'..'
            elif(len(artist)>16):
                artist_edited = artist[0:(40-len(song)-2)]+'..'
            else:
                song_edited = song[0:(40-len(artist)-2)]+'..'
        return song_edited + " - " + artist_edited
    else:
        song_edited=song
        artist_edited=artist
        if(len(song)+len(artist)>26):
            if(len(artist)>10 and len(song)>16):
                artist_edited = artist[0:8]+'..'
                song_edited=song[0:14]+'..'
            elif(len(artist)>10):
                artist_edited = artist[0:(26-len(song)-2)]+'..'
            else:
                song_edited = song[0:(26-len(artist)-2)]+'..'
        return song_edited + " - " + artist_edited

class AwesomeStatusBarApp(rumps.App):
    length = 'Short'
    current_song=["",""]
    
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__(
            name="Playful",
            title="Now Playing",
            icon="icons/spotify.png",
            menu=[
                'Play / Pause',
                'Next',
                'Previous',
                None,
                {'Text Length':
                    ['Short', 'Long']
                }
            ],
            quit_button=None
        )
        try:
            self.length = config['PlayfulPy']['length']
        except:
            self.length = 'Short'
        def refresh_title():
            if(isRunning() == 'running'):
                try:
                    track = getCurrentTrack()
                    # print(track)
                    # print(" and ")
                    # print(self.current_song)
                    if(track[0]!=self.current_song[0] or track[1]!=self.current_song[1]):
                        # print("copying")
                        self.current_song=track.copy()
                        self.title = formatTitle(track[0], track[1], self.length)
                except:
                    self.current_song = ['', '']
                    self.title = "Error"
            else:
                self.current_song = ['', '']
                self.title = "Open Spotify"
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
    
    
    @rumps.clicked("Text Length", 'Short')
    def format_length_short(self, _):
        self.length='Short'
        self.refresh_title_once()
    
    @rumps.clicked("Text Length", 'Long')
    def format_length_long(self, _):
        self.length='Long'
        self.refresh_title_once()
    
    @rumps.clicked('Quit')
    def save_on_quit(self, _):
        config['PlayfulPy'] = {
            'length': self.length
        }
        with open('PlayfulPy.ini', 'w') as configfile:
            config.write(configfile)
        rumps.quit_application()
    
    def refresh_title_once(self):
            try:
                track = getCurrentTrack();
                self.current_song=track.copy()
                self.title = formatTitle(track[0], track[1], self.length)
            except:
                pass
    
if __name__ == "__main__":
    AwesomeStatusBarApp().run()
