from django.conf import settings
# import ConfigParser
import urllib.parse
import random
import base64
import hmac
import binascii
import time
import collections
import hashlib
import requests
import json
import string
import secrets
import pprint

def escape(s):
    """Percent Encode the passed in string"""
    return urllib.parse.quote(s, safe='~')


def get_nonce():
    """Unique token generated for each request"""
    letters = ''.join(secrets.choice(string.ascii_letters) for i in range(32))
    n = base64.b64encode(letters.encode('utf-8'))
    return n


def generate_signature(method, url, url_parameters, oauth_parameters,
                       oauth_consumer_key, oauth_consumer_secret,
                       oauth_token_secret=None, status=None):
    """Create the signature base string"""

    #Combine parameters into one hash
    temp = collect_parameters(oauth_parameters, status, url_parameters)

    #Create string of combined url and oauth parameters
    parameter_string = stringify_parameters(temp)

    #Create your Signature Base String
    signature_base_string = (
        method.upper() + '&' +
        escape(str(url)) + '&' +
        escape(parameter_string)
    )

    #Get the signing key
    signing_key = create_signing_key(oauth_consumer_secret, oauth_token_secret)

    return calculate_signature(signing_key, signature_base_string)

def collect_parameters(oauth_parameters, status, url_parameters):
    """Combines oauth, url and status parameters"""
    #Add the oauth_parameters to temp hash
    temp = oauth_parameters.copy()

    #Add the status, if passed in.  Used for posting a new tweet
    if status is not None:
        temp['status'] = status

    #Add the url_parameters to the temp hash
    for k, v in url_parameters.items():
        temp[k] = v

    return temp


def calculate_signature(signing_key, signature_base_string):
    """Calculate the signature using SHA1"""
    hashed = hmac.new(signing_key.encode('utf-8'), signature_base_string.encode('utf-8'), hashlib.sha1)

    sig = binascii.b2a_base64(hashed.digest())[:-1]

    return escape(sig)


def create_signing_key(oauth_consumer_secret, oauth_token_secret=None):
    """Create key to sign request with"""
    signing_key = escape(oauth_consumer_secret) + '&'

    if oauth_token_secret is not None:
        signing_key += escape(oauth_token_secret)

    return signing_key


def create_auth_header(parameters):
    """For all collected parameters, order them and create auth header"""
    ordered_parameters = {}
    ordered_parameters = collections.OrderedDict(sorted(parameters.items()))
    auth_header = (
        '%s="%s"' % (k, v) for k, v in ordered_parameters.items())
    val = "OAuth " + ', '.join(auth_header)
    return val


def stringify_parameters(parameters):
    """Orders parameters, and generates string representation of parameters"""
    output = ''
    ordered_parameters = {}
    ordered_parameters = collections.OrderedDict(sorted(parameters.items()))

    counter = 1
    for k, v in ordered_parameters.items():
        output += escape(str(k)) + '=' + escape(str(v))
        if counter < len(ordered_parameters):
            output += '&'
            counter += 1

    return output


def get_oauth_parameters(consumer_key, access_token):
    """Returns OAuth parameters needed for making request"""
    oauth_parameters = {
        'oauth_timestamp': str(int(time.time())),
        'oauth_signature_method': "HMAC-SHA1",
        'oauth_version': "1.0",
        'oauth_token': access_token,
        'oauth_nonce': get_nonce(),
        'oauth_consumer_key': consumer_key
    }

    return oauth_parameters
    

if __name__ == '__main__':
    
    #method, url and parameters to call
    method = "get"
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    url_parameters = {
        'exclude_replies': 'true'
    }

    # settings = settings.configure()
    # #configuration hash for the keys
    # CONSUMER_API_SECRET_KEY = settings.CONSUMER_API_SECRET_KEY
    # CONSUMER_API_KEY = settings.CONSUMER_API_KEY
    # ACCESS_TOKEN = settings.ACCESS_TOKEN
    # ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET

    CONSUMER_API_KEY = 'hmzsUAijyLhuTyMMnG6Hzysn8'
    CONSUMER_API_SECRET_KEY = 'KIuE21pBHIsSmbn8GalXhYREybF8qcTDPevGVZEkBsOyHZQsMG'
    ACCESS_TOKEN = 'nZnvfVdzhuXGSrAYE92H7eicI2DAgFrP756DXdVG7mvE4'
    ACCESS_TOKEN_SECRET = 'nZnvfVdzhuXGSrAYE92H7eicI2DAgFrP756DXdVG7mvE4'


    keys = {
        "twitter_consumer_secret": CONSUMER_API_SECRET_KEY,
        "twitter_consumer_key": CONSUMER_API_KEY,
        "access_token": ACCESS_TOKEN,
        "access_token_secret": ACCESS_TOKEN_SECRET
    }

    oauth_parameters = get_oauth_parameters(
        keys['twitter_consumer_key'],
        keys['access_token']
    )

    oauth_parameters['oauth_signature'] = generate_signature(
        method,
        url,
        url_parameters, oauth_parameters,
        keys['twitter_consumer_key'],
        keys['twitter_consumer_secret'],
        keys['access_token_secret']
    )
    pprint.pprint(oauth_parameters)

    headers = {'Authorization': create_auth_header(oauth_parameters)}

    url += '?' + urllib.parse.urlencode(url_parameters)

    r = requests.get(url, headers=headers)
    print(r)
    results = json.dumps(json.loads(r.text), sort_keys=False, indent=4)
    print(results)

    

