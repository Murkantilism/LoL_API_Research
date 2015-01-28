__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse

# Setup RiotWatcher object with api key
api = RiotWatcher('17dd8043-3e16-4cad-a388-985bfd93d275')

summoner_data = []

def main():
    global summoner_data

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
             s_data = api.get_ranked_stats(tmp_id, region=None, season=None)
             summoner_data.append(s_data)
        except LoLException:
            print 'DATA NOT FOUND FOR SUMMONER ' + str(tmp_id)

def write_summoner_data(inputLocation):
    with open("_out_"+inputLocation+".txt", 'w') as file:
        for summoner in summoner_data:
            file.writelines(str(summoner)+"\n\n\n")

if __name__ == "__main__":
    main()