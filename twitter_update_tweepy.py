#!/usr/bin/env python
"""Python method to send updates to twitter."""
import sys
import tweepy

consumer_key='xx'
consumer_secret='xx'
access_key='xx'
access_secret='xx'

if not access_key:
  auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth_url = auth.get_authorization_url()
  print 'Please authorize: ' + auth_url
  verifier = raw_input('PIN: ').strip()
  auth.get_access_token(verifier)
  print "ACCESS_KEY = '%s'" % auth.access_token.key
  print "ACCESS_SECRET = '%s'" % auth.access_token.secret
else:
  auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_key, access_secret)
  api=tweepy.API(auth)
  if len(sys.argv)==1:
    msg=raw_input("Status: ")
  else:
    msg=sys.argv[1]
  api.update_status(msg)
