__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse, time
from operator import itemgetter

# Setup RiotWatcher object with api key
f = open('apikey.txt', 'r')
api = RiotWatcher(f.read())

allChampionsUsed = []

f = open('loChampionPairs', 'r')
champions = f.read()
champions = champions.splitlines()

summoner_name_id_dict = {}

summoner_most_used_champ_dict = {}

def main():
    global summoner_name_id_dict
    global summoner_most_used_champ_dict
    global allChampionsUsed

    # Command line parsing
    global inputLocation
    global outputLocation

    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners.')

    parser.add_argument('-in', metavar='i', type=str)
    parser.add_argument('-out', metavar='o', type=str)

    args = parser.parse_args()

    print vars(args).values()
    outputLocation = vars(args).values()[0]
    inputLocation = vars(args).values()[1]

    # Check if we have API calls remaining
    createDictOfSummoners()

    # For every key in the dict, get the summoner stats
    for k in summoner_name_id_dict:
        getSummonerStats(k, summoner_name_id_dict.get(k))

    # For every key value pair in the dict of most used champs, write data
    #for k, v in summoner_most_used_champ_dict.iteritems():
    #    writeMostUsedChampion(k, v)

    print "MOST USED CHAMPIONS FOUND"

# Read the input txt file and create a dictionary of summoners.
# Dict format is {summonerId: summonerName} since summoners cannot have the same ID
# but could possibly have the same username across different region servers.
def createDictOfSummoners():
    f = open(inputLocation, 'r')
    read_input = f.readlines()
    for i, line in enumerate(read_input):
        # Append the summoner ID minus last 2 characters (\n) and summoner name to dict
        summoner_name_id_dict.update({line.split(":")[1][:-1]: line.split(":")[0]})

# Get the ranked stats of the given summoner ID
def getSummonerStats(summoner_id, summoner_name):

    # 1 second buffer
    if not api.can_make_request():
        time.sleep(1)

    try:
        summoner_stats = api.get_ranked_stats(summoner_id, region=None, season=None)
    except LoLException:
        print "GAME DATA NOT FOUND FOR SUMMONER: " + str(summoner_id)
        summoner_stats = "{u'modifyDate': 1406927571000L, u'summonerId': 0000, u'champions': [{u'stats': {u'totalPhysicalDamageDealt': 152101, u'totalTurretsKilled': 1, u'totalSessionsPlayed': 1000, u'totalAssists': 10, u'totalDamageDealt': 158764, u'mostChampionKillsPerSession': 2, u'totalPentaKills': 0, u'mostSpellsCast': 0, u'totalDoubleKills': 0, u'maxChampionsKilled': 2, u'totalDeathsPerSession': 8, u'totalSessionsWon': 0, u'totalGoldEarned': 12405, u'totalTripleKills': 0, u'totalChampionKills': 2, u'maxNumDeaths': 8, u'totalMinionKills': 199, u'totalMagicDamageDealt': 5315, u'totalQuadraKills': 0, u'totalUnrealKills': 0, u'totalDamageTaken': 17519, u'totalSessionsLost': 1, u'totalFirstBlood': 0}, u'id': XX}, 2]}"
        summoner_id += "XX"

    parseSummonerStats(summoner_stats, summoner_id, summoner_name)

# Given the ranked stats, parse it to get the totalSessionsPlayed and
# corresponding champion id value
def parseSummonerStats(summoner_stats, summoner_id, summoner_name):
    summoner_stats = str(summoner_stats).split(', {')

    start = "'totalSessionsPlayed': "
    end = ", u'totalAssists"

    start1 = "u'id': "
    end1 = "}"

    for s in summoner_stats:
        # Get the number of totalSessionsPlayed
        result = re.search("%s(.*)%s" % (start, end), str(s)).group(1)
        # And the corresponding champion
        result1 = re.search("%s(.*)%s" % (start1, end1), str(s)).group(1)
        # And create a pair [totalSessionsPlayed, id]
        allChampionsUsed.append([result, result1])

    sortChampions(summoner_id, summoner_name)

# Sort the list of all champions used by this summoner based on the number
# of totalSessionsPlayed (which is the first value in the pair)
def sortChampions(summoner_id, summoner_name):
    allChampionsUsed_sorted = sorted(allChampionsUsed, key=itemgetter(0))

    # Pass only the LAST pair to getChampionTitle (most used champion!)
    getChampionTitle(allChampionsUsed_sorted[-1], summoner_id, summoner_name)
    #print str(summoner_id) + " most used champ: " + str(allChampionsUsed_sorted[-1])

# Given a champion ID, look at the loChampionPairs file to get it's
# corresponding champion title
def getChampionTitle(mostUsedChampionPair, summoner_id, summoner_name):
    # For every champion in loChampionPairs, get the most used champ's title
    for line in champions:
        line = line.split(' | ')
        if line[0] == mostUsedChampionPair[1]:
            if summoner_id.__contains__("XX"):
                mostUsedChampion = "GAME DATA NOT FOUND"
            else:
                mostUsedChampion = line[1]
                summoner_most_used_champ_dict.update({summoner_id: str(summoner_name)+":"+mostUsedChampion})
                writeMostUsedChampion(summoner_id, str(summoner_name)+":"+mostUsedChampion)
            print "MOST USED CHAMPION FOR ID #" + str(summoner_id).strip("XX") +\
                  " IS: " + str(mostUsedChampion)

# Write the most used champion to output file
def writeMostUsedChampion(summoner_id, summoner_name_and_champ):
    with open(outputLocation, 'a') as file:
        file.writelines(summoner_id + ":" + summoner_name_and_champ + "\n")

if __name__ == "__main__":
    main()