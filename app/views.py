# -*- coding: utf-8 -*-

from flask import Flask, make_response, render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app
from urllib import urlopen

from itertools import chain
IPN_URLSTRING = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
IPN_VERIFY_EXTRA_PARAMS = (('cmd', '_notify-validate'),)


@app.route('/')
def index():
	return "Hello Paypal"
def ordered_storage(f):
    import werkzeug.datastructures
    import flask
    def decorator(*args, **kwargs):
        flask.request.parameter_storage_class = werkzeug.datastructures.ImmutableOrderedMultiDict
        return f(*args, **kwargs)
    return decorator

@app.route('/paypal/', methods=['POST'])
@ordered_storage
def paypal_webhook():
    
    #probably should have a sanity check here on the size of the form data to guard against DoS attacks
    received_args = chain(request.form.iteritems(), IPN_VERIFY_EXTRA_PARAMS)
    verify_string = '&'.join(('%s=%s' % (param, value) for param, value in received_args))
    #req = Request(verify_string)
    response = urlopen(IPN_URLSTRING, data=verify_string)
    status = response.read()
    print status
    if status == 'VERIFIED':
        print "PayPal transaction was verified successfully."
        # Do something with the verified transaction details.
        payer_email =  request.form.get('payer_email')
        print "Pulled {email} from transaction".format(email=payer_email)
    else:
        print "status is %s"%status
        print 'Paypal IPN string did not validate:\n {arg}'.format(arg=verify_string)

    return jsonify({'status':'complete'})
