# script to manage spotify authorization for spotify accounts
# see spotify_auth_flow.pdf for further insight
#
# Caden Johnson - 6/14/22

# import necessary libraries
from requests import Request, post

# import necessary objects
from credentials import CLIENT_ID, SECRET_ID, REDIRECT_URI

class AuthURL():
    def get(self, request, format=None):
        scopes = ''
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_url': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return url

        

# Begin Authorization
# Request authorization to access data
# client_id, response_type, redirect_uri, state, scope

    # recieve code, state from User

# Request access and refresh tokens
# client_id, client_secret, grant_type, code, redirect_uri

    # recieve access_token, token_type, expires_in, refresh_token from Spotify



# LOOP
# Use access token in requests to web api
# access_token

    # recieve JSON object
    # and sometimes new access_token????
