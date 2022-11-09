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


# Custom Auth class to carry out Authorization Code Flow
class CusAuth:
    def __init__(self, client_id=CLIENT_ID, client_secret=SECRET_ID, redirect_uri=REDIRECT_URI, scope=SCOPE):
        self.client_id = client_id
        # example of why python has limited inheritance security... can still be
        # accessed, although more difficult (auth._CusAuth__client_secret)
        #self.__clientsecret = client_secret
        self.client_creds_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode())
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = None
        self.acc_token = None
        self.ref_token = None
        self.expires = None
        self.valid_request = None
        self.token_url="https://accounts.spotify.com/api/token"
        self.auth_url="https://accounts.spotify.com/authorize"


    # stage 2 request to api for access tokens
    def req_acc_n_ref_tokens(self, code):
        print('Its an error with stage 2')
        token_response_data = requests.post(self.token_url, 
        data={
            'grant_type': "authorization_code",
            'code': code,
            'redirect_uri': self.redirect_uri
        }, 
        headers={
            'Authorization': f"Basic {self.client_creds_b64.decode()}",
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        print(token_response_data)

        if validate(token_response_data):
            token_data = token_response_data.json()
            self.access_token = token_data['access_token']
            self.ref_token = token_data['refresh_token']
            self.scope = token_data['scope']
            expires_in = token_data['expires_in']
            self.expires = create_expires(expires_in)

            print(self.ref_token, self.acc_token, self.expires, self.scope)
            return self.ref_token, self.acc_token, self.expires, self.scope
        print('error 3')
        return False


    # stage 3 request for refresh token
    def refresh_token(self, ref_token):
        token_response_data = requests.post(self.token_url, 
        data={
            'grant_type': "refresh_token",
            'refresh_token': ref_token,
        }, 
        headers={
            'Authorization': f"Basic {self.client_creds_b64.decode()}",
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        if validate(token_response_data):
            token_data = token_response_data.json()
            if token_data['refresh_token']:
                self.ref_token = token_data['refresh_token']
            self.acc_token = token_data['access_token']
            self.scope = token_data['scope']
            expires_in = token_data['expires_in']
            self.expires = create_expires(expires_in)

            return self.ref_token, self.acc_token, self.expires, self.scope
        print('error 4')
        return False


# stage 3
def Reinitialize_Spotify(r_token):
    auth_object = CusAuth(CLIENT_ID, SECRET_ID, REDIRECT_URI, SCOPE)
    rdata = auth_object.refresh_token(r_token)
    return rdata

