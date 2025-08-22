#!/bin/python3

"""
https://codeforces.com/blog/entry/143815
"""

import requests
import json
import math
import random
import sys

contestid = sys.argv[1] if len(sys.argv) >= 2 else input("contestid: ")
result = requests.get("https://codeforces.com/api/contest.standings?contestId="+contestid+"&showUnofficial=true&participantTypes=CONTESTANT,VIRTUAL,OUT_OF_COMPETITION").json()["result"]
problems = result["problems"]
standings = result["rows"]
numusers = len(standings)

def cf_color(r: int) -> str:
    """
    Return ANSI escape code for a given Codeforces rating.
    Colors match the CF palette: grey, green, cyan, blue, purple, orange, red.
    (LGM 3000+ shown as bold red.)
    """
    # Basic ANSI colors
    GREY    = "\033[90m"
    GREEN   = "\033[32m"
    CYAN    = "\033[36m"
    BLUE    = "\033[34m"
    PURPLE  = "\033[35m"
    ORANGE  = "\033[38;5;208m"  # 256-color "orange"
    RED     = "\033[31m"
    BOLDRED = "\033[38;5;124m"  # 256-color "darker red"

    if r < 1200:
        return GREY          # Newbie
    if r < 1400:
        return GREEN         # Pupil
    if r < 1600:
        return CYAN          # Specialist
    if r < 1900:
        return BLUE          # Expert
    if r < 2100:
        return PURPLE        # Candidate Master
    if r < 2400:
        return ORANGE        # Master / International Master
    if r < 3000:
        return RED           # Grandmaster / International Grandmaster
    return BOLDRED           # Legendary Grandmaster (3000+)

def colorize_number(n: int) -> str:
    RESET = "\033[0m"
    return f"{cf_color(n)}■ {n:>4}{RESET}"

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
# print(pctsolved)
diff = [avgrating for i in problems]
for i in range(len(problems)):
    # diff[i] = 800 - 400*math.log((1-pow(0.5,(3500-avgrating)/400))*pctsolved[i]+pow(0.5,(800/(400-avgrating))*(-2700/400)))/math.log(pow(0.5,800/(400-avgrating)))
    diff[i] = 800 - 400*math.log((1-pow(0.5,(3500-avgrating)/400))*pctsolved[i]+pow(0.5,(3500-avgrating)/400))/math.log(pow(0.5,400/(800-avgrating)))
for i in range(len(problems)):
    link = "https://codeforces.com/gym/" + contestid + "/problem/" + problems[i]["index"]
    print(f"{problems[i]['index']:<2}", colorize_number(round(diff[i]/50)*50), f"{pctsolved[i]*100:>5.2f}%", problems[i]["name"])
