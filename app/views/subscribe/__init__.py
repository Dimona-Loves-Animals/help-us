# -*- coding: utf-8 -*-

from flask import request, redirect
from app.utils import *
from app import app;
from app.views import *
import json
import mailchimp

list_id = app.config['MAILCHIMP_LIST_ID']

@app.route("/subscribes", methods=['GET',])
def subscribes():
    subscribers = 0
    try:
	# get mailchimp api instance
        m = get_mailchimp_api()
        subscribers = m.lists.members(list_id)
    except:
	pass
    return str(subscribers['total'])

@app.route("/subscribe", methods=['GET',])
def subscribe_page():
    return render.template('subscribe', subscribers_count = subscribes())

@app.route("/subscribe", methods=['POST',])
def subscribe():
    # get email from form
    email = request.form['email']
    try:
	# get mailchimp api instance
        m = get_mailchimp_api()
        m.lists.subscribe(list_id, {'email':email})
        if request.is_xhr:
    	    return json.dumps({'status': 'success'});
    except mailchimp.ListAlreadySubscribedError:
        return json.dumps({'status': 'error', 'data': 'כתובת דואר אלקטרוני זו כבר רשומה במערכת. תודה על ההרשמה.'})
    except mailchimp.Error, e:
	return json.dumps({'status': 'error', 'data': 'An error occurred: %s - %s' % (e.__class__, e) })
    return redirect('/')