__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse, os

# Setup RiotWatcher object with api key
api = RiotWatcher('17dd8043-3e16-4cad-a388-985bfd93d275')

summoner_data = []
summoner_ids = []

def main():
    global summoner_data
    global summoner_ids

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

    print "DATA FOR " + str(len(summoner_data)) + " SUMMONERS ACQUIRED"


def get_summoner_data(summoners_list):
    start = "'id': "
    end = ", '"

    for summoner in summoners_list:
        # Get the summoner ID
        tmp_id = re.search("%s(.*)%s" % (start, end), str(summoner)).group(1)

        # Try to retrieved the summoner data for the ID we just got
        try:
             s_data = api._match_history_request(tmp_id+"?beginIndex=15&endIndex=30", region=None)
             # If we get data back, append the ID to array and data to another
             summoner_ids.append(tmp_id)
             summoner_data.append(s_data)
        except LoLException:
            print 'DATA NOT FOUND FOR SUMMONER ' + str(tmp_id)

# Write the summoner data, writing a new file for each summoner
def write_summoner_data(inputLocation):
    for summoner in summoner_data:
        for id in summoner_ids:
            file = open(os.curdir+"\_out2\_"+id+"_"+inputLocation+".txt", 'w')
            file.writelines(str(summoner)+"\n\n\n")

if __name__ == "__main__":
    main()