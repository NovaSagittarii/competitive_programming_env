#!/bin/python3

"""
https://codeforces.com/blog/entry/143815
"""

import requests
import json
import math
import random
 
contestid = input("contestid: ")
result = requests.get("https://codeforces.com/api/contest.standings?contestId="+contestid+"&showUnofficial=true&participantTypes=CONTESTANT,VIRTUAL,OUT_OF_COMPETITION").json()["result"]
problems = result["problems"]
standings = result["rows"]
numusers = len(standings)
 
numsolved = []
for i in range(len(problems)):
    numsolved.append(0)
for i in standings:
    for j in range(len(problems)):
        if i["problemResults"][j]["points"] > 0:
            numsolved[j] += 1
 
avgrating = 1200
#avgrating = 1125 for div 2
#avgrating = 1200 for div 1 + div 2
#don't use this for harder contests where the majority of participants are master+
pctsolved = [i/numusers for i in numsolved]
print(pctsolved)
diff = [avgrating for i in problems]
for i in range(len(problems)):
    # diff[i] = 800 - 400*math.log((1-pow(0.5,(3500-avgrating)/400))*pctsolved[i]+pow(0.5,(800/(400-avgrating))*(-2700/400)))/math.log(pow(0.5,800/(400-avgrating)))
    diff[i] = 800 - 400*math.log((1-pow(0.5,(3500-avgrating)/400))*pctsolved[i]+pow(0.5,(3500-avgrating)/400))/math.log(pow(0.5,400/(800-avgrating)))
for i in range(len(problems)):
    link = "https://codeforces.com/gym/" + contestid + "/problem/" + problems[i]["index"]
    print(f"{round(diff[i]):>4}", problems[i]["name"])
