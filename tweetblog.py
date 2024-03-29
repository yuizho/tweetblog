#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flask_oauth import OAuth
from database import db_session
from models import Entries, Stack
import sys
import datetime
import traceback
import json
from convertmonth import convert

DEBUG      = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

oauth = OAuth()

consumer_args = open('consumer.csv').readlines()[0].split(',')
consumer_key_str = consumer_args[0]
consumer_secret_str = consumer_args[1]

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1.1/',
                           request_token_url='http://api.twitter.com/oauth/request_token',
                           access_token_url='http://api.twitter.com/oauth/access_token',
                           authorize_url='http://api.twitter.com/oauth/authorize',
                           consumer_key=consumer_key_str,
                           consumer_secret=consumer_secret_str
)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.before_request
def before_request():
   pass

@app.after_request
def after_request(response):
    return response

@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_token')

@app.route('/')
def show_entries():
    entries = {}
    image = ""
    try:
        resp = twitter.get('statuses/user_timeline.json')
        if resp.status == 200:
            tweets = resp.data
            #画像アドレス取得
            image = tweets[0]['user']['profile_image_url_https']

            json.dump(resp.data, open('output.json', 'w'), sort_keys=True, indent=4, )
            
            tweetdate = ''
            tweetdatearray = []
            for i in tweets:
                for k, v in i.iteritems():
                    if k == 'created_at':
                        datearray = v.split(' ')
                        tweetdate = (datearray[5] + '/' + convert(datearray[1]) + '/' + datearray[2])
                        tweetdatearray.append(tweetdate)
                        if not entries.has_key(tweetdate):
                            entries[tweetdate] = []
            
            num = 0                
            for i in tweets:
                
                text = ''
                media_url = ''
                geo_lat = '' #緯度
                geo_lng = '' #経度
                for k, v in i.iteritems():
                    
                    if k == 'text':
                        text = v
                    elif k == 'entities':
                        if v.get("media") is not None:
                            for mv in v.get("media"):
                                if mv.get("type") == "photo":
                                    media_url = mv.get("media_url")
                    elif k == "coordinates":
                        if v is not None:
                            geo_lat = v.get("coordinates")[1]
                            geo_lng = v.get("coordinates")[0]
                            print geo_lng
                            print geo_lat
                entries[tweetdatearray[num]].append(dict(content = text, image = media_url, lat = geo_lat, lng = geo_lng))
                print entries
                num += 1
            
            #タプルに変換してsort
            entries = [(k, entries[k]) for k in sorted(entries, reverse = True)]
        else:
            entries = None
            flash('Unable to load tweets from Twitter. Maybe out of '
                  'API calls or Twitter is overloaded.')
    except:
        print traceback.format_exc()
    return render_template('show_entries.html', entries=entries, image=image)

@app.route('/login')
def login():
    sys.stderr.write(url_for("oauth_authorized"))
    return twitter.authorize(callback=url_for("oauth_authorized"))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('twitter_token', None)
    session["logged_in"] = None
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = url_for('show_entries')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['username'] = resp['screen_name']
    flash(resp['screen_name'] + ' were signed in')
    session["logged_in"] = True
    session['user_id'] = int(resp['user_id'])
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    return redirect(next_url)

if __name__ == '__main__':
    app.run('0.0.0.0')
