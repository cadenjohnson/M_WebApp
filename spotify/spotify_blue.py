# script responsible for routes associated with the spotify API
#
# Play that funky music white boi - 11/5/2022

from flask import Blueprint, redirect, request, render_template
from app import db, current_user
from M_models import Spotifym
from flask_login import login_required
import spotify.M_S_authenticate as AUTH
import spotipy
import spotify.M_S_operate as Operate


spotify = Blueprint('spotify', __name__, template_folder = 'templates')


def indexauth(spot_account):
    # check whether the access token is expired
    if AUTH.check_expiration(spot_account.expires) or spot_account.access_token == None:
    # if it is, carry out stage 3 to obtain access token
        rdata = AUTH.use_refresh_token(spot_account.refresh_token)

        if not rdata:
            return False
        else:
            ref_token, acc_token, expires, scope = rdata
            print(ref_token,' | ',acc_token,' | ',expires,' | ',scope)

        # update database with new data
        if ref_token != None:
            spot_account.refresh_token = ref_token
        spot_account.access_token = acc_token
        spot_account.expires = expires
        spot_account.scope = scope
        try:
            db.session.commit()
        except:
            return False

        return True
    return True



# index page
@spotify.route('/', methods=['POST','GET'])
@login_required
def index():
    if request.method == 'GET':
        # check if valid account registered with McKraken
        spot_account = Spotifym.query.filter_by(user_id=current_user.id).first()
        if spot_account and spot_account.user_id == current_user.id:
            # assist w checks and updates
            success = indexauth(spot_account)
            if success:
                # test case - display the playlists
                playlists = Operate.get_playlists(spot_account.access_token)
                return render_template('spotify_dash.html', playlists=playlists, error=('Logged In. Access Token= '+str(spot_account.access_token)))

            else:
                return render_template('errorpage.html', error='Error with GET request for index')
        
        # assume they dont have an account registered yet
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
        the_url = "https://accounts.spotify.com/authorize?scope="+str(AUTH.SCOPE)+"&redirect_uri="+str(AUTH.REDIRECT_URI)+"&response_type=code&client_id="+str(AUTH.CLIENT_ID)+"&state="+str(state) 

        return redirect(the_url)
    else:
        return render_template('errorpage.html', error='Error with POST request for index')



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
                data = AUTH.get_tokens(code)

                ref_token, acc_token, expires, scope = data
                # update database with tokens etc
                if acc_token == None:
                    data = AUTH.use_refresh_token(ref_token)
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

    return redirect('/spotify')



@spotify.route('/delete')
@login_required
def delete():
    account_to_delete = Spotifym.query.filter_by(user_id=current_user.id).first()
    if account_to_delete:
        try:
            db.session.delete(account_to_delete)
            db.session.commit()
            return redirect('/spotify')

        except:
            return render_template('errorpage.html', error='Error while attempting to delete account')


