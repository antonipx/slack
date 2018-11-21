#
# list members of a channel, takes channel name as argument
#

import os
import sys
import re
from slackclient import SlackClient

kf=open(".apikeya", "r")
apitok=kf.readline().rstrip()
kf.close()

sc=SlackClient(apitok)



chan=sc.api_call("conversations.list", exclude_archived=1, limit=1000, types="public_channel,private_channel")
for c in chan['channels']:
    print c['name'], c['id']

