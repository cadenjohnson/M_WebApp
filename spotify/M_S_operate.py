# scripts to operate spotify account via spotipy
# simple scripts like skip, play, etc.
#
# Caden Johnson - 11/9/2022

import json, requests
from flask import jsonify

# just for references...
#import spotipy
#sp = spotipy.Spotify(auth=acc_token)

global prefix
prefix = "https://api.spotify.com/v1"


# must return as a json object
def playback_state(acc_token):
    try:
        url = prefix+"/me/player"
        headers={
            "Authorization": f"Bearer {acc_token}",
            "Content-Type": "application/json"
            }

        playback = (requests.get(url=url, headers=headers)).json()
        print(playback)
        # return device, track, shuffle, repeat, isplaying, albumimage
        if "device" in playback:
            device = playback['device']['name']
        else:
            device = None
        if "item" in playback:
            track = playback['item']['name']
            artist = playback['item']['artists'][0]['name']
            try:
                albumcover = playback['item']['album']['images'][1]['url']
            except:
                albumcover = None
        else:
            track = None
        shuffle = playback['shuffle_state']
        repeat = playback['repeat_state']
        is_playing = playback['is_playing']

        result = {
            'success': True,
            'device': device,
            'track': track,
            'artist': artist,
            'shuffle': shuffle,
            'repeat': repeat,
            'isplaying': is_playing,
            'albumcover': albumcover
        }

        print(result)
        return result
    except:
        return {'success':'False', 'message':'error getting current state'}



def play(acc_token):
    try:
        url = prefix+"/me/player/play"
        headers={
            "Authorization": f"Bearer {acc_token}",
            "Content-Type": "application/json"
            }

        test = requests.put(url=url, headers=headers)
        if test:
            return {'success':'True'}
        if test.status_code == 404:
            return {'success':'False', 'message':'404 No Active Devices'}
    except:
        return {'success':'False', 'message':'error playing'}



def pause(acc_token):
    try:
        url = prefix+"/me/player/pause"
        headers={
            "Authorization": f"Bearer {acc_token}",
            "Content-Type": "application/json"
            }

        test = requests.put(url=url, headers=headers)
        if test:
            return {'success':'True'}
        if test.status_code == 404:
            return {'success':'False', 'message':'404 No Active Devices'}
    except:
        return {'success':'False', 'message':'error pausing'}



def previous(acc_token):
    try:
        url = prefix+"/me/player/previous"
        headers={
            "Authorization": f"Bearer {acc_token}",
            "Content-Type": "application/json"
            }

        test = requests.post(url=url, headers=headers)
        if test:
            return {'success':'True'}
        if test.status_code == 404:
            return {'success':'False', 'message':'404 No Active Devices'}
    except:
        return {'success':'False', 'message':'error skipping to previous'}



def next(acc_token):
    try:
        url = prefix+"/me/player/next"
        headers={
            "Authorization": f"Bearer {acc_token}",
            "Content-Type": "application/json"
            }

        test = requests.post(url=url, headers=headers)
        if test:
            return {'success':'True'}
        if test.status_code == 404:
            return {'success':'False', 'message':'404 No Active Devices'}
    except:
        return {'success':'False', 'message':'error skipping to next'}



def shuffle_toggle(acc_token):
    pass



def get_devices(acc_token):
    try:
        url = prefix+"/me/player/devices"
        headers={
            "Authorization": f"Bearer {acc_token}",
            "Content-Type": "application/json"
            }

        devices = (requests.get(url=url, headers=headers)).json()
        device_array = []

        for i, device in enumerate(devices['devices']):
            temp = ("%4d |  %s" % (i + 1, device['name']))
            device_array.append(temp)

        return device_array
    except:
        return ['Error getting devices']



def get_playlists(acc_token):
    try:
        url = prefix+"/me/playlists"
        headers={
            "Authorization": f"Bearer {acc_token}",
            "Content-Type": "application/json"
            }

        playlists = (requests.get(url=url, headers=headers)).json()
        play_array = []

        for i, playlist in enumerate(playlists['items']):
            temp = ("%4d |  %s" % (i + 1 + playlists['offset'], playlist['name']))
            play_array.append(temp)

        return play_array
    except:
        return ['Error getting playlists']



def get_currently_playing(acc_token):
    pass

def search_for_song(song, acc_token):
    pass

def search_for_artist(artist, acc_token):
    pass

