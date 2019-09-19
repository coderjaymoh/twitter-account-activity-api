from django.conf import settings
import base64
import hashlib
import hmac
import json
import requests

class Notify:
    listener_url = settings.LISTENER_URL
    register_url = settings.ACTIVITY_API_URL
    access_token = settings.ACCESS_TOKEN
    consumer_api_key = settings.CONSUMER_API_KEY

    def oauth_nonce(self, stringLenth = 32):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))

    def register_url(self):
        url = self.register_url
        headers = {
            "Authorization": 'OAuth oauth_consumer_key="%s", oauth_nonce="GENERATED", oauth_signature="GENERATED", oauth_signature_method="HMAC-SHA1", oauth_timestamp="GENERATED", oauth_token="%s", oauth_version="1.0" % self.consumer_api_key, self.access_token',
            "Content-Type": "application/json"
        }
        body = {
            "url": "%s" % self.listener_url 
        }

        reg_url_response = requests.post(url, json=body, headers=headers)

        return reg_url_response


    def token(self, CONSUMER_API_SECRET_KEY, msg):
        # creates HMAC SHA-256 hash from incomming token and your consumer secret
        sha256_hash_digest = hmac.new(CONSUMER_API_SECRET_KEY, msg=msg, digestmod=hashlib.sha256).digest()

        
        print(sha256_hash_digest)    

        # construct response data with base64 encoded hash
        response = {
            'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest)
        }

        print(response)


        # returns properly formatted json response
        return json.dumps(response)
  


# curl --request POST --url 'https://api.twitter.com/1.1/account_activity/webhooks.json?url=https://24072e23.ngrok.io/api/webhook/twitter' --header 'authorization: OAuth oauth_consumer_key="hmzsUAijyLhuTyMMnG6Hzysn8", oauth_nonce="GENERATED", oauth_signature="GENERATED", oauth_signature_method="HMAC-SHA1", oauth_timestamp="GENERATED", oauth_token="3156199463-Wx5p2RfNimZcPQZyQknh0GTas1XxYxlGSUWM8NR", oauth_version="1.0"'