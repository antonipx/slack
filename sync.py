#
# add users from source channel to channels matching regex
# note sleeps are important as slack api is rate limited
#

import os
import re
import time
from slackclient import SlackClient

source_channel_name="support-internal"
channels_re=".*-(premium|support|supp)$"

kf=open(".apikey", "r")
apitok=kf.readline().rstrip()
kf.close()

sc=SlackClient(apitok)

# find id for the source channel
chan=sc.api_call("conversations.list", exclude_archived=1, limit=1000, types="public_channel,private_channel")
for c in chan['channels']:
    if c['name'] == source_channel_name:
        print "Source Channel:", c['name'], "id:", c['id']
        src_id=c['id']
        break

src=sc.api_call("conversations.members", channel=src_id, limit=1000)

# sync members for matching channels
chan=sc.api_call("conversations.list", exclude_archived=1, limit=1000, types="public_channel,private_channel")
for c in chan['channels']:
    if re.match(channels_re, c['name']):
        #print c['name'], c['id']
        time.sleep(0.5)
        cm=sc.api_call("conversations.members", channel=c['id'], limit=1000)
        for src_m in src['members']:
            match=False
            for cmm in cm['members']:
                if src_m==cmm:
                    match=True
            if match==False:
                print "  adding", src_m, "to", c['name'], c['id']
                ret=sc.api_call("conversations.invite", channel=c['id'], users=src_m)
                if ret['ok'] == False:
                    print "    ", ret['errors']
                time.sleep(2)
                 
