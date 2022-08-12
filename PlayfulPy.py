from time import sleep
import rumps
import threading
from functions import *
import configparser
from multiprocessing import Process
from flask import Flask, request
import webbrowser
import requests
import base64


config = configparser.ConfigParser()
config.read('PlayfulPy.ini')
client_id = config['PlayfulPy']['client_id']
client_secret = config['PlayfulPy']['client_secret']
redirect_uri = config['PlayfulPy']['redirect_uri']
uri_port = config['PlayfulPy']['uri_port']
refresh_token = config['PlayfulPy']['refresh_token'] if 'refresh_token' in config['PlayfulPy'] else None
server_instance = None
code=None
spot_instance = None
auth_instance = None
timer = None
access_token = None

scope = [
    "user-read-currently-playing",
    "user-read-playback-state",
    "user-modify-playback-state",
];

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

def Server():
        app = Flask("MyServer")
        webbrowser.open(('''https://accounts.spotify.com/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}''').format(client_id=client_id, redirect_uri=redirect_uri, scope=",".join(scope)))
        
        @app.before_first_request
        def before_first_request():
            print("Opened window")
        
        def shutdown_server():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @app.after_request
        def after_request(res):
            shutdown_server()
            return res

        @app.route("/")
        def getCode():
            global code
            code = request.args['code']
            print(request.args['code'])
            return "<p>Hello, code: !</p> " + request.args['code']
        app.run(host='localhost', port=config['PlayfulPy']['uri_port'])

def getAccessToken():
    res = requests.post("https://accounts.spotify.com/api/token", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization":
        "Basic " +
        base64.b64encode((client_id + ":" + client_secret).encode("ascii")).decode('ascii'),
    },
    params={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    })
    res = res.json()
    global access_token
    global refresh_token
    global timer        
    access_token=res['access_token']
    refresh_token=res['refresh_token']

    timer=res['expires_in']
def getRefreshToken():
    res = requests.post("https://accounts.spotify.com/api/token", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization":
        "Basic " +
        base64.b64encode((client_id + ":" + client_secret).encode("ascii")).decode('ascii'),
    },
    params={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    })
    res = res.json()
    global access_token
    global timer
    access_token=res['access_token']
    timer=res['expires_in']

def handleSignIn():
    try:
        if(refresh_token==None):
            print("handling server")
            Server()
            getAccessToken()
        else:
            try:
                getRefreshToken()
            except:
                print("handling server")
                Server()
                getAccessToken()
        PlayfulPy.source = 'connect'
        
    except Exception as e:
        print('Error while signing in')
        print(e)

class PlayfulPy(rumps.App):
    length = 'Short'
    current_song=["",""]
    send_notification = False
    source = 'spotify'  # spotify | connect
    def __init__(self):
        super(PlayfulPy, self).__init__(
            name="Playful",
            title="Now Playing",
            icon="icons/spotify.png",
            menu=[
                'Play / Pause',
                'Next',
                'Previous',
                None,
                {'Options':
                    [{
                        'Text Length':['Short', 'Long'],
                        'Source': ['Spotify App', 'Spotify Connect (Experimental)'],
                        'Send Notification On Change' : ['On', 'Off']
                    },
                    ]
                }
            ],
            quit_button=None
        )
        
        try:
            if('send_notification' in config['PlayfulPy']):
                PlayfulPy.send_notification = config['PlayfulPy']['send_notification']=='True'
            if('length' in config['PlayfulPy']):
                PlayfulPy.length = config['PlayfulPy']['length']
            if('source' in config['PlayfulPy']):
                PlayfulPy.source = config['PlayfulPy']['source']
        except:
            pass
        def refresh_title():
            # print(PlayfulPy.source)
            # print(PlayfulPy.current_song)
            if(PlayfulPy.source=='spotify'):
                if(isRunning() == 'running'):
                    try:
                        track = getCurrentTrack()
                        # print(track)
                        # print(" and ")
                        # print(self.current_song)
                        if(track[0]!=PlayfulPy.current_song[0] or track[1]!=PlayfulPy.current_song[1]):
                            # print("copying"x)
                            if(PlayfulPy.send_notification==True):
                                PlayfulPy.send_notification and rumps.notification(title=track[0], message=track[1], subtitle="")
                            PlayfulPy.current_song=track.copy()
                            self.title = formatTitle(track[0], track[1], PlayfulPy.length)
                            
                    except:
                        PlayfulPy.current_song = ['', '']
                        self.title = "Error"
                else:
                    PlayfulPy.current_song = ['', '']
                    self.title = "Open Spotify"
            else:
                try:
                    track = getCurrentTrack(access_token)
                    # print(track)
                    # print(" and ")
                    # print(self.current_song)
                    if(track[0]!=PlayfulPy.current_song[0] or track[1]!=PlayfulPy.current_song[1]):
                        # print("copying")
                        if(PlayfulPy.send_notification==True):
                            rumps.notification(title=track[0], message=track[1], subtitle="")
                        PlayfulPy.current_song=track.copy()
                        self.title = formatTitle(track[0], track[1], PlayfulPy.length)
                except Exception as e:
                    self.current_song = ['', '']
                    self.title = "Could Not Get Song"
                    print(e)
            threading.Timer(2.0, refresh_title).start()
        refresh_title()
        
    @rumps.clicked("Options", "Source", "Spotify Connect (Experimental)")
    def spotify_app(self, _):
        x = threading.Thread(target=handleSignIn)
        x.start()
    
    @rumps.clicked("Options", "Source", "Spotify App")
    def spotify_connect(self, _):
        PlayfulPy.source="spotify"
        
    @rumps.clicked("Options", "Send Notification On Change", "On")
    def send_notification_on(self, _):
        PlayfulPy.send_notification = True
    
    @rumps.clicked("Options", "Send Notification On Change", "Off")
    def send_notification_off(self, _):
        PlayfulPy.send_notification = False

    @rumps.clicked("Play / Pause")
    def toggle(self, _):
        if(PlayfulPy.source=='spotify'):
            if(getState()=="playing"):
                pause()
            else:
                play()
        else:
            if(getState(access_token)=='playing'):
                pause(access_token)
            else:
                play(access_token)

    @rumps.clicked("Next")
    def skip_next(self, _):
        if(PlayfulPy.source=='spotify'):
            next()
        else:
            next(access_token)
        self.refresh_title_once()

    @rumps.clicked("Previous")
    def skip_prev(self, _):
        if(PlayfulPy.source=='spotify'):
            previous()
        else:
            previous(access_token)
        self.refresh_title_once()
    
    
    @rumps.clicked("Options", "Text Length", 'Short')
    def format_length_short(self, _):
        PlayfulPy.length='Short'
        self.refresh_title_once()
    
    @rumps.clicked("Options", "Text Length", 'Long')
    def format_length_long(self, _):
        PlayfulPy.length='Long'
        self.refresh_title_once()
    
    @rumps.clicked('Quit')
    def save_on_quit(self, _):
        config['PlayfulPy']['length'] = PlayfulPy.length
        config['PlayfulPy']['send_notification'] = str(PlayfulPy.send_notification)
        config['PlayfulPy']['source'] = PlayfulPy.source
        if(refresh_token!=None):
            config['PlayfulPy']['refresh_token'] = refresh_token
        with open('PlayfulPy.ini', 'w+') as configfile:
            config.write(configfile)
        rumps.quit_application()
    
    def refresh_title_once(self):
        if(PlayfulPy.source=='spotify'):
            try:
                track = getCurrentTrack()
                PlayfulPy.current_song=track.copy()
                self.title = formatTitle(track[0], track[1], PlayfulPy.length)
            except:
                pass
        else:
            try:
                track = getCurrentTrack(access_token)
                PlayfulPy.current_song=track.copy()
                self.title = formatTitle(track[0], track[1], PlayfulPy.length)
            except:
                pass
            
    
if __name__ == "__main__":
    PlayfulPy().run()
