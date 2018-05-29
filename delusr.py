#
# delete user from support channels
#

import os
import sys
import re
import time
from slackclient import SlackClient

source_channel_name="support-internal"
channels_re=".*-(premium|support)$"

kf=open("apikey", "r")
apitok=kf.readline().rstrip()
kf.close()

sc=SlackClient(apitok)

if len(sys.argv)<2:
    print "usage:", sys.argv[0], "user_id"
    exit()


sc=SlackClient(legacy_api_token)

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
    if re.match(channels_re, c['name']) or c['name'] == source_channel_name:
        print "  removing", sys.argv[1], "from", c['name'], c['id']
        ret=sc.api_call("conversations.kick", channel=c['id'], user=sys.argv[1])
        if ret['ok'] == False:
            print "    ", ret['errors']
        time.sleep(10)
                 
