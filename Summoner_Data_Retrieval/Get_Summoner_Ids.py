__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse, time

# Setup RiotWatcher object with api key
f = open('apikey.txt', 'r')
api = RiotWatcher(f.read())

numSummonersWritten = 0

summonerDict = {}
def main():

    # Command line parsing
    global outputLocation
    global summonerDict

    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners.')

    parser.add_argument('-in', metavar='i', type=str)
    parser.add_argument('-out', metavar='o', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[1]
    outputLocation = vars(args).values()[0]

    f = open(inputLocation, "r")
    summoners = f.readlines()

    # For every summoner in the text file (NOTE: We slice the last 2 chars of each line '\n' newline)
    for s in summoners:
        # Check if we have API calls remaining
        if(api.can_make_request()):
            # Get it's ID, append it to dict. Returns true if id is found, false otherwise
            if Get_Summoner_Ids(s[:-1]) == True:
                # Check to make sure it's a real summoner
                if Check_Summoner(s[:-1]) == True:
                    # Check the summoner's level is 30
                    if Check_Level(s[:-1]) == True:
                        Write_Summoner(s[:-1])
                        '''
                        # Check the summoner's rank's is gold/plat
                        if Check_Rank(s[:-1]) == True:
                            # If all tests pass, write summoner to out
                            Write_Summoner(s[:-1])
                        # If not right rank, remove it from dict
                        else:
                            summonerDict.pop(str(s[:-1]))
                        '''
                    # If not lvl 30 remove it from dict
                    else:
                        summonerDict.pop(str(s[:-1]))
                # If not real summoner remove it from dict
                else:
                    summonerDict.pop(str(s[:-1]))
            # If no data is returned, do nothing
            else:
                pass
        # If no api call remain, wait 5 seconds
        else:
            print "API: Waiting 10 seconds for more API calls..."
            time.sleep(10)

    print "OUT: " + str(numSummonersWritten) + " summoner IDs retrieved."

# Given a summoner string name, get the summoner id
def Get_Summoner_Ids(summoner):

    # Get the summoner object
    try:
        summonerObj = api.get_summoner(name=summoner, _id=None, region=None)
    except LoLException:
        print "Summoner " + summoner + " not found."
        return False

    # Define search terms
    start = "u'id': "
    end = ", u'name':"

    # Search json for summoner id
    summoner_id = re.search("%s(.*)%s" % (start, end), str(summonerObj)).group(1)

    # Append summoner string and id to a dict
    summonerDict.update({str(summoner): str(summoner_id)})

    return True

# Check if the summoner name is good
# This is to avoid summoners like: IS148be5be2f2d180191298
def Check_Summoner(summoner):
    if summoner[0:3].__contains__("IS1"):
        print("Summoner " + str(summoner) + ":" + str(summonerDict[str(summoner)]) + " has been culled (fake)")
        return False
    else:
        print "Summoner " + str(summoner) + ":" + str(summonerDict[str(summoner)]) + " Exists!"

        return True

# Check if summoner is level 30
def Check_Level(summoner):

    start = "u'summonerLevel': "
    end = ", u'revisionDate"

    if(api.can_make_request()):
        check_level = api.get_summoner(name=None, _id=summonerDict[str(summoner)], region=None)

        result = re.search("%s(.*)%s" % (start, end), str(check_level)).group(1)

        if (str(result) == "30"):
            return True
        else:
            return False
    else:
        print "API: Wating 10 seconds for more API calls..."
        time.sleep(10)
        Check_Level(summoner) # Recursive call to try again


# Checks if the given summoner is in Gold or Platinum
def Check_Rank(summoner):
    try:
        print "Checking: " + str(summonerDict[str(summoner)])
        check_rank = api.get_league_entry(str(summonerDict[str(summoner)]), team_ids=None, region=None)
    except LoLException:
        print "Summoner ID " + str(summonerDict[str(summoner)]) + " is not in any leagues."
        return False

    # Only check the first 40 characters (in case GOLD is in username/elsewhere)
    if str(check_rank)[0:40].__contains__("GOLD") | \
       str(check_rank)[0:40].__contains__("PLATINUM"):
        print "RANK: " + str(check_rank)
        return True
    else:
        print("Summoner ID " + str(summonerDict[str(summoner)]) + " is not in GOLD or PLATINUM")
        return False

# Write the dict of summoners to a text document
def Write_Summoner(summoner):
    f = open(outputLocation, 'a') # Open file in append mode instead of write!
    f.write(str(summoner)+":"+str(summonerDict[str(summoner)])+"\n")
    global numSummonersWritten
    numSummonersWritten += 1
    f.close()

if __name__ == "__main__":
    main()