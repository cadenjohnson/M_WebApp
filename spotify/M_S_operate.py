# scripts to operate spotify account via spotipy
# simple scripts like skip, play, etc.
#
# Caden Johnson - 11/9/2022

import json, requests

# just for references...
import spotipy
sp = spotipy.Spotify(auth=acc_token)


def prep_request(url, payload, params, acc_token):
    prefix="https://api.spotify.com/v1/"
    url = prefix + url
    args = dict(params=params)
    headers={"Authorization": "Bearer {0}".format(acc_token)}

    if "content_type" in args["params"]:
        headers["Content-Type"] = args["params"]["content_type"]
        del args["params"]["content_type"]
        if payload:
            data = payload
    else:
        headers["Content-Type"] = "application/json"
        if payload:
            args["data"] = json.dumps(payload)

    session = requests.Session()
    try:
        if data:
            response = requests.get(url=url, data=data, headers=headers)
        else:
            response = requests.get(url=url, headers=headers)
        return response
    except:
        return False



def play(acc_token):
    pass

def pause(acc_token):
    pass

def shuffle_toggle(acc_token):
    pass

def get_devices(acc_token):
    pass

def get_playlists(acc_token):
    pass

def get_currently_playing(acc_token):
    pass

def search_for_song(song, acc_token):
    pass

def search_for_artist(artist, acc_token):
    pass

