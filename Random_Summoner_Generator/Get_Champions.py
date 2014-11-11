__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re

# Setup RiotWatcher object with api key
api = RiotWatcher('17dd8043-3e16-4cad-a388-985bfd93d275')

list_of_champion_ids = []

def main():
    # Check if we have API calls remaining
    if(api.can_make_request()):
        #getListOfIDs()
        #sortIDs()
        sortIDs()


# Gets a list of Champion ID's from riot's API (unsorted strings)
def getListOfIDs():
    champions = api.get_all_champions(region=None, free_to_play=False)

    # Above string has lots of info we don't care about
    champions = str(champions).split(", {")
    # Look for only ID's
    start = "id': "
    end = "}"

    f = open('loChampionIDs', 'a')

    # For every element in champions, get the string in between start and end
    for champ in champions:
        result = re.search("%s(.*)%s" % (start, end), str(champ)).group(1)
        print(result)
        f.write(str(result) +'\n')
        f.close()

# Look through the list of unsorted ID strings, sort them as ints
def sortIDs():
    f = open('loChampionIDs', 'r')
    champs = f.read()
    champs = champs.split('\n')
    champs = [int(x) for x in champs]
    champs.sort()

    f = open('loChampionIDs_sorted', 'a')

    f.write(str(champs))
    print champs
    pairChampions(champs)

# Look through the list of sorted ID strings, get the static champion info
# based on the ID, and create a text file of pairs: ID | Champion Name
def pairChampions(champs):
    f = open('loChampionPairs', 'a')
    for champ in champs:
        champ_info = api.static_get_champion(champ)

        # Lots of info we don't care about, get just the key (champion name)
        start = "'key': u'"
        end = "',"
        result = re.search("%s(.*)%s" % (start, end), str(champ_info)).group(1)

        print champ_info

        f.write(str(champ) + " | " + str(result) + "\n")

    f.close()

if __name__ == "__main__":
    main()