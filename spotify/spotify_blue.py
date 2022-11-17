# script responsible for routes associated with the spotify API
#
# Play that funky music white boi - 11/5/2022

from flask import Blueprint, redirect, request, render_template, jsonify
from app import db, current_user
from M_models import Spotifym
from flask_login import login_required
import spotify.M_S_authenticate as AUTH
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
                # display the playlists and devices
                playlists = Operate.get_playlists(spot_account.access_token)
                devices = Operate.get_devices(spot_account.access_token)
                return render_template('spotify_dash.html', playlists=playlists, devices=devices, atoken=str(spot_account.access_token))

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



@spotify.route('/delete', methods=['GET','POST'])
@login_required
def delete():
    if request.method == 'GET':
        return render_template('verify_choice.html', route='/spotify/delete', message='Are you sure you want to un-Register your Spotify account?')
    elif request.method == 'POST':
        account_to_delete = Spotifym.query.filter_by(user_id=current_user.id).first()
        if account_to_delete:
            try:
                db.session.delete(account_to_delete)
                db.session.commit()
                return redirect('/spotify')

            except:
                return render_template('errorpage.html', error='Error while attempting to delete account')
    else:
        return render_template('errorpage.html', error='Error. Incorect request method')



# basically a proxy between client and spotify
@spotify.route('/play', methods=['POST'])
#@login_required
def play():
    if request.method == 'POST':
        # Recieve access token
        try:
            data = request.json
            access_token = data['atoken']

            # validate access token
            spot_account = Spotifym.query.filter_by(access_token=access_token).first()
            if spot_account:
                success = indexauth(spot_account)
                if success:
                    if data['action'] == 'pause':
                        return jsonify({'success':'False'})
                        # pause call to api
                        test = Operate.pause(spot_account.access_token)
                    elif data['action'] == 'play':
                        # play call to api
                        test = Operate.play(spot_account.access_token)
                    
                    if test['success'] == 'True':
                        # current state call to api
                        playback = Operate.playback_state(spot_account.access_token)
                        
                        # return json data
                        return jsonify(playback)
                    else:
                        return jsonify(test)
        except:
            return jsonify({'success':'False'})

    return jsonify({'success':'False'})


