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


# find id for the channel
u=sc.api_call("users.list", limit=1000)
for m in u['members']:
        print m['id'], m['name'], m['profile']['real_name']
        if(m['deleted'] == False):
            print m['is_restricted']
