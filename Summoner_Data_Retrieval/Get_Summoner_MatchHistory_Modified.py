__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse, os, time

# Setup RiotWatcher object with api key
f = open('apikey.txt', 'r')
api_key = f.read()
api = RiotWatcher(f.read())

match_history_data = []

def main():
    global match_history_data

    parser = argparse.ArgumentParser(description='Attempt to grab data for given list of summoners.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    # Read a list of lines into data
    file = open(inputLocation, 'r')
    read_input = file.readlines()

    # Check if we have API calls remaining
    if(api.can_make_request()):
        get_summoner_data(read_input)

    write_summoner_data(inputLocation)

    print "DATA FOR " + str(len(match_history_data)) + " SUMMONERS ACQUIRED"


def get_summoner_data(summoners_list):
    start = "`"
    end = ":"

    for summoner in summoners_list:
        # Get the summoner ID
        tmp_id = re.search("%s(.*)%s" % (start, end), str(summoner)).group(1)

        # Try to retrieve the summoner data for the ID we just got
        if api.can_make_request():
            try:
                s_data = api._match_history_request(end_url=tmp_id+"?includeTimeline=true&beginIndex=16&endIndex=31&api_key="+str(api_key), region=None)
                match_history_data.append("`"+str(tmp_id)+"`:"+str(s_data))
                print 'DATA FOUND FOR SUMMONER ' + str(tmp_id)
            except LoLException:
                print 'ERR: DATA NOT FOUND FOR SUMMONER ' + str(tmp_id)
        else:
            print "API: Waiting 5 seconds for more calls"
            time.sleep(5)

# Write the summoner data, writing a new file for each summoner
def write_summoner_data(inputLocation):
    start = "`"
    end = "`:"

    for summoner in match_history_data:
        # Get the summoner id again, used to write individual files for each summoner
        tmp_id = re.search("%s(.*)%s" % (start, end), str(summoner)).group(1)
        # Write summoner data to output folder
        with open(os.curdir+"\_outMatchHistory_16to31\_"+tmp_id+"_"+inputLocation, 'w') as writeFile:
            writeFile.writelines(str(summoner)+r"\n")

if __name__ == "__main__":
    main()