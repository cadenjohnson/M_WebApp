# script responsible for routes associated with the spotify API
#
# Play that funky music white boi - 11/5/2022

from flask import Blueprint, redirect, request, render_template
from app import db, current_user
from M_models import Spotifym
from flask_login import login_required
import spotify.M_S_authenticate as AUTH


spotify = Blueprint('spotify', __name__, template_folder = 'templates')


# index page
@spotify.route('/', methods=['POST','GET'])
@login_required
def index():
    if request.method == 'GET':
        # check if user has a refresh token associated with their account
        spot_account = Spotifym.query.filter_by(user_id=current_user.id).first()

        print(spot_account)
        if spot_account and spot_account.user_id == current_user.id:
            # if they do, check whether the access token is expired
            if AUTH.check_expiration(spot_account.expires):
            # if it is, carry out stage 3 to obtain access token
                rdata = AUTH.Reinitialize_Spotify(spot_account.refresh_token)

                if not rdata:
                    return render_template('errorpage.html', error='1')
                else:
                    ref_token, acc_token, expires, scope = rdata

                # update database with new data
                spot_account.refresh_token = ref_token
                spot_account.access_token = acc_token
                spot_account.expires = expires
                spot_account.scope = scope
                try:
                    db.session.commit()
                except:
                    return render_template('errorpage.html', error='2')

                # then display dashboard
                # using new access token
                return render_template('spotify_dash.html', error=('Logged In. Access Token= '+spot_account.access_token))
            else:
                # using old access token
                return render_template('spotify_dash.html', error=('Logged In. Access Token= '+spot_account.access_token))
        
        # assume they dont have an account registered yet
        # display button with link to endpoint that begins stage 1 to gain authorization
        # button will send POST request which is routed below
        return render_template('spotify_dash.html')

    # for POST requests
    elif request.method == 'POST':
        state = AUTH.get_state()

        # update database with new account
        new_account = Spotifym(
            user_id=current_user.id,
            state = state)
        try:
            db.session.add(new_account)
            db.session.commit()
        except:
            return render_template('errorpage.html', error='4')

        # basically stage 1 (part 1)
        #response = requests.get("https://accounts.spotify.com/authorize", params={
        #    'client_id': AUTH.CLIENT_ID,
        #    'response_type': 'code',
        #    'redirect_url': AUTH.REDIRECT_URI,
        #    'state': state,
        #    'scope': AUTH.SCOPE
        #})
        the_url = "https://accounts.spotify.com/authorize?scope="+str(AUTH.SCOPE)+"&redirect_uri="+str(AUTH.REDIRECT_URI)+"&response_type=code&client_id="+str(AUTH.CLIENT_ID)+"&state="+str(state) 

        return redirect(the_url)
    else:
        return render_template('errorpage.html', error='6')


# https://127.0.0.1:5000/spotify/spotauth?code=AQCm8EdJoPJFVySAeTE5kLUTNyaRNM9L4wz70ZV3TM5qzUBDGhofmO1TWN5AgK7DRI58J4XJqkMG81Eieq5jsCtJi1vY44EtNGsSIHNJtspCLrXRQPgcFxwXilUzPr9BRDbfjEspamMsqejEbjUoRNm95S_lOQ1VTopGg0oTCXZLCsisz1hH6CEdfWgS0lW5WxqJrx4TLICJquFfVx3rqyiBh_pETVPb7bbuFKY0qEiOGz-b7RMoc7-lyDNwfc98_UvLLE6jr4oUm996txND0PD185TxsVOOip-1ihOTG-UgdOslY--QeiwcqNzy2D8dxmZWMyIfGkMwjr9E3AKyQqxFY7E92F7Pew&state=None

# stage 1 (part 2) used to obtain code and state
@spotify.route('/spotauth')
@login_required
def spotauth():
    # obtain code and state
    params = request.args
    params = params.to_dict()

    spot_account = Spotifym.query.filter_by(user_id=current_user.id).first()

    try:
        if params['code']:
            code = params['code']

            # validate state and move on to stage 2
            if spot_account.state == params['state']:
                Auth_Object = AUTH.CusAuth()
                data = Auth_Object.req_acc_n_ref_tokens(code)

                # update database with tokens etc
                ref_token, acc_token, expires, scope = data
                spot_account.refresh_token = ref_token
                spot_account.access_token = acc_token
                spot_account.expires = expires
                spot_account.is_expired = False
                spot_account.scope = scope
                try:
                    db.session.commit()
                except:
                    return render_template('errorpage.html', error='2')
            else:
                return render_template('errorpage.html', error='4')
        else:
            return render_template('errorpage.html', error='6')
    except:
        return render_template('errorpage.html', error='7')

    return render_template('spotify_dash.html', error='Logged In!')


