__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse, os, time
import urllib2

# Setup RiotWatcher object with api key
f = open('apikey.txt', 'r')
api_key = f.read()
api = RiotWatcher(f.read())

match_history_data = []
match_ids = []
match_data = []

def main():
    global match_history_data
    global match_ids
    global match_data

    parser = argparse.ArgumentParser(description='Attempt to grab match data for given list of summoners.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    # Read a list of lines into data
    file = open(inputLocation, 'r')
    match_history_data = file.readlines()

    # First find the summoner ID for this match
    summoner_id = get_summoner_id(inputLocation)

    # Split up the match history (which is all 1 line) by the matchID string
    match_history_split = str(match_history_data).split("u'matchId")

    # Pop off first element of array (doesn't contain any match ID's)
    match_history_split.pop(0)

    # Get the 15 match ID's in the given match history file
    get_match_ids(match_history_split)

    # Get the match data!
    get_match_data_HTTPS(match_ids, summoner_id)

    # Write match data
    #write_summoner_data(inputLocation, match_data, summoner_id)

    print "DATA FOR " + str(len(match_data)) + " MATCHES ACQUIRED"


# Given the input location, search for the top level folder and summoner
# summoner id. Lop off the top level folder, leaving just the summoner id.
def get_summoner_id(inputLocation):
    # Define search terms to get match ID
    start = "\_"
    end = "__out"

    summoner_id = re.search("%s(.*)%s" % (start, end), str(inputLocation)).group(1)

    return summoner_id[23:]

# Given match history data, find all 15 matchID's and store in array
def get_match_ids(match_history_data):
    # Define search terms to get match ID
    start = "': "
    end = ", u'mapId':"

    # For each element of the match history array
    for match in match_history_data:
        # Lop off everything past 25 characters (doesn't include matchID!)
        match = match[:25]
        # Search for the match ID
        tmp_id = re.search("%s(.*)%s" % (start, end), str(match)).group(1)
        #print "MATCH ID: " + str(tmp_id)
        match_ids.append(tmp_id)

    if not (len(match_ids) == 15):
        print "WARN: " + str(len(match_ids)) + " MATCH IDs FOUND"
    else:
        print str(len(match_ids)) + " MATCH IDs FOUND"

# An ugly workaround for the 401 unauthorized error Riot API is giving get_match() call
# Open the match https URL and read the data, feed it to write_summoner_data()
def get_match_data_HTTPS(match_ids, summoner_id):
    for id in match_ids:
        response = urllib2.urlopen("https://na.api.pvp.net/api/lol/na/v2.2/match/"+str(id)+"?includeTimeline=true&api_key="+str(api_key))
        write_summoner_data(response.read(), summoner_id)

'''
This function, for some reason, returns a 401 unauthorized error. It should be a problem
with the API key or URL being passed, but neither seem to be incorrect. API key works fine,
URL could be wrong if there's a bug in RiotWatcher but otherwise should be good. See hack
function above that replaces this one.

def get_match_data(match_ids):
    for id in match_ids:
        # Try to retrieve the match data for each id
        if api.can_make_request():
            #try:
            m_data = api.get_match(match_id=id, region=None, include_timeline=True)
            match_data.append(str(m_data))
            print 'DATA FOUND FOR MATCH ID ' + str(id)
            #except LoLException:
            #    print 'ERR: DATA NOT FOUND FOR MATCH ID ' + str(id)
        else:
            print "API: Waiting 5 seconds for more calls"
            time.sleep(5)
'''

# Write the match data, writing a new file for each summoner ID
def write_summoner_data(match_data, summoner_id):
    # Write summoner data to output folder
    with open(os.curdir+"\_outMatchData_0to15\_"+summoner_id, 'a') as writeFile:
        writeFile.writelines(str(match_data))

if __name__ == "__main__":
    main()