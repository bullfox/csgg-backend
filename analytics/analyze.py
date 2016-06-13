import json
import sys

def matchwinrate(champ1, champ2):
    i=0
    i2=0
    with open("raw_matchups", "r") as data:
        for line in data:
            outcome = line.strip("\n").split(">")
            if int(outcome[0]) == champ1 and int(outcome[1]) == champ2:
                i+=1
            if int(outcome[0]) == champ2 and int(outcome[1]) == champ1:
                i2+=1
        print(i)
        print(i2)
    return ((i / (i2 + i)) * 100)

def getchamp(champ_name):
    with open('champdata.json') as sfile:
        champ_json = json.load(sfile)
        obj = champ_json['data'][champ_name]
    return(obj['id'])


print(matchwinrate(getchamp(sys.argv[1]), getchamp(sys.argv[2])))
