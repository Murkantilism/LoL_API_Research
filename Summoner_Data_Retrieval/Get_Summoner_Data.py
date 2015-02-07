__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse, os

# Setup RiotWatcher object with api key
f = open('apikey.txt', 'r')
api = RiotWatcher(f.read())

match_data = []

def main():
    global match_data

    parser = argparse.ArgumentParser(description='Attempt to grab data for given list of summoners.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    # Read a list of lines into data
    file = open(inputLocation+".txt", 'r')
    summoners_list = file.readlines()

    # Check if we have API calls remaining
    if(api.can_make_request()):
            get_summoner_data(summoners_list)

    write_summoner_data(inputLocation)

    print "DATA FOR " + str(len(match_data)) + " SUMMONERS ACQUIRED"


def get_summoner_data(summoners_list):
    start = "'id': "
    end = ", '"

    for summoner in summoners_list:
        # Get the summoner ID
        tmp_id = re.search("%s(.*)%s" % (start, end), str(summoner)).group(1)

        # Try to retrieve the summoner data for the ID we just got
        try:
             #s_data = api.get_match_history(summoner_id=tmp_id, region=None, champion_ids=None, ranked_queues=None, begin_index=0, end_index=15)
             s_data = api._match_history_request(end_url=tmp_id+"?includeTimeline=true&beginIndex=0&endIndex=15&api_key=17dd8043-3e16-4cad-a388-985bfd93d275", region=None)
             match_data.append("'id': "+tmp_id+", ' "+str(s_data))
        except LoLException:
            print 'DATA NOT FOUND FOR SUMMONER ' + str(tmp_id)

# Write the summoner data, writing a new file for each summoner
def write_summoner_data(inputLocation):
    start = "'id': "
    end = ", '"

    for summoner in match_data:
        # Get the summoner id again, used to write individual files for each summoner
        tmp_id = re.search("%s(.*)%s" % (start, end), str(summoner)).group(1)
        # Write summoner data to output folder
        file = open(os.curdir+"\_outGendered\_"+tmp_id+"_"+inputLocation+".txt", 'w')
        file.writelines(str(summoner)+"\n\n\n")

if __name__ == "__main__":
    main()