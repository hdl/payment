# -*- coding: utf-8 -*-

from flask import Flask, make_response, render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app
from urllib import urlopen, urlencode, quote_plus
import requests

from itertools import chain
IPN_URLSTRING = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
IPN_VERIFY_EXTRA_PARAMS = (('cmd', '_notify-validate'),)
from itertools import chain

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
    verify_args = chain(IPN_VERIFY_EXTRA_PARAMS, request.form.iteritems())
    verify_string = '&'.join(('%s=%s' % (param, quote_plus(value.encode('utf-8'), safe=':/')) for param, value in verify_args))
    print request.form
    print verify_string
    response = urlopen(IPN_URLSTRING+'?'+verify_string)
    status = response.read()
    print status
    if status == 'VERIFIED':
        print "PayPal transaction was verified successfully."
        # Do something with the verified transaction details.
        payer_email =  request.form.get('payer_email')
        print "Pulled {email} from transaction".format(email=payer_email)
    else:
         print 'Paypal IPN string {arg} did not validate'.format(arg=verify_string)

    return jsonify({'status':'complete'})
