import oauth2 as oauth
import urllib2 as urllib
import json

# See Assignment 1 instructions or README for how to get these credentials
access_token_key = "945954878517665793-qfO9BH7BHXghfqfJlIgSHDf5pKeBhgm"
access_token_secret = "ylZDolthuNPoCuCOONacmhnXXfVfORP4QbTZBdPED6iBn"

consumer_key = "fzWsvSA2mN6y13YgYQR9lq6XD"
consumer_secret = "dpxi0Fv5fhFc1rcd3ZjdDvf5bAIXsv0k5JnXTvMboqCiSBaA5w"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1.1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  #with open('tweets.json', 'w') as json_file:
  for tweet in response:
    print(tweet.strip())

if __name__ == '__main__':
  fetchsamples()
