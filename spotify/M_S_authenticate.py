# script to manage spotify authorization for spotify accounts
# see spotify_auth_flow.pdf for further insight
#
# Caden Johnson - 6/14/22
#
# Update - Fuck it... spotipy sucks, imma do it myself - 11/5/2022
#
# stage 1 - request authentication
# stage 2 - request access token, refresh token, etc
# stage 3 - request new tokens due to expired access token

# import necessary libraries
import requests, string, random, base64, datetime

# import necessary objects
from spotify.credentials import CLIENT_ID, SECRET_ID, REDIRECT_URI, SCOPE
global client_creds_b64 
client_creds_b64 = base64.b64encode(f"{CLIENT_ID}:{SECRET_ID}".encode())


def get_state():
    # generate a random, non-guessable string
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(6))


# check whether the access token has expired
def check_expiration(expires):
    return expires < datetime.datetime.now()


# create expires attribute
def create_expires(exp_in):
    now = datetime.datetime.now()
    return (now + datetime.timedelta(seconds=exp_in))


# check whether response is valid
def validate(response):
    return response.status_code in range(200, 299)




# stage 2 request to api for access tokens
def get_tokens(code):
    token_response_data = requests.post("https://accounts.spotify.com/api/token", 
    data={
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': REDIRECT_URI
    }, 
    headers={
        'Authorization': f"Basic {client_creds_b64.decode()}",
        'Content-Type': 'application/x-www-form-urlencoded'
    })

    if validate(token_response_data):
        token_data = token_response_data.json()
        acc_token = token_data['access_token']
        ref_token = token_data['refresh_token']
        scope = token_data['scope']
        expires_in = token_data['expires_in']
        expires = create_expires(expires_in)

        return ref_token, acc_token, expires, scope
    return False




# stage 3 request for refresh token
def use_refresh_token(ref_token):
    token_response_data = requests.post("https://accounts.spotify.com/api/token", 
    data={
        'grant_type': "refresh_token",
        'refresh_token': ref_token,
    }, 
    headers={
        'Authorization': f"Basic {client_creds_b64.decode()}",
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    
    if validate(token_response_data):
        token_data = token_response_data.json()
        if 'refresh_token' in token_data:
            if token_data['refresh_token'] and token_data['refresh_token'] != None:
                ref_token = token_data['refresh_token']
        acc_token = token_data['access_token']
        scope = token_data['scope']
        expires_in = token_data['expires_in']
        expires = create_expires(expires_in)

        return ref_token, acc_token, expires, scope

    return False



