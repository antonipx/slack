#
# list members of a channel, takes channel name as argument
#

import os
import sys
import re
from slackclient import SlackClient

kf=open("apikey", "r")
apitok=kf.readline().rstrip()
kf.close()

sc=SlackClient(apitok)

if len(sys.argv)<2:
    print "usage:", sys.argv[0], "<channel name>"
    exit()


# find id for the channel
chan=sc.api_call("conversations.list", exclude_archived=1, limit=1000, types="public_channel,private_channel")
for c in chan['channels']:
    if c['name'] == sys.argv[1]:
        print c['name'], "id:", c['id']
        id=c['id']
        break

chan=sc.api_call("conversations.members", channel=id, limit=1000)
print "Members:"

for m in chan['members']:
    mm=sc.api_call("users.info", user=m)
    u=mm['user']
    p=u['profile']
    print("  %-15s %-15s %-15s %s" % (m, u['name'], p['display_name_normalized'], p['email']))

