import os
import sys
import re
from slackclient import SlackClient

kf=open(".apikey", "r")
apitok=kf.readline().rstrip()
kf.close()

sc=SlackClient(apitok)

chan=sc.api_call("conversations.list", exclude_archived=1, limit=1000, types="public_channel,private_channel")
for c in chan['channels']:
    if re.match(".*-(premium|support|supp)$", c['name']):
        print c['name'], ":"
        cm=sc.api_call("conversations.members", channel=c['id'], limit=1000)
        for m in cm['members']:
            ui=sc.api_call("users.info", user=m)
            try:
                if "portworx.com" not in ui['user']['profile']['email']:
                    print " ", ui['user']['profile']['id'], ui['user']['profile']['email']
            except:
                pass
