__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re
from operator import itemgetter

# Setup RiotWatcher object with api key
api = RiotWatcher('17dd8043-3e16-4cad-a388-985bfd93d275')

allChampionsUsed = []

f = open('loChampionPairs', 'r')
champions = f.read()
champions = champions.splitlines()

with open('_out/Random_Summoners_run12.txt', 'r') as file:
    # read a list of lines into data
    random_summoners_1k = file.readlines()

def main():
    # Check if we have API calls remaining
    if(api.can_make_request()):
        getSummoners()

        # Keyword: u'id':
        # Keyword: u'totalSessionsPlayed':
    print "MOST USED CHAMPIONS FOUND"

def getSummoners():
    f = open('_out/Random_Summoners_run12.txt', 'r')
    summoners = f.read()
    summoners = summoners.splitlines()

    for s in summoners:
        # Lots of info we don't care about, get just the key (champion name)
        start = "'id': "
        end = ", '"
        result = re.search("%s(.*)%s" % (start, end), str(s)).group(1)
        getSummonerStats(result)


# Get the ranked stats of the given summoner
def getSummonerStats(summoner_id):
    try:
        summoner_stats = api.get_ranked_stats(summoner_id, region=None, season=None)
    except LoLException:
        #print "GAME DATA NOT FOUND FOR SUMMONER: " + str(summoner_id)
        summoner_stats = "{u'modifyDate': 1406927571000L, u'summonerId': 0000, u'champions': [{u'stats': {u'totalPhysicalDamageDealt': 152101, u'totalTurretsKilled': 1, u'totalSessionsPlayed': 1000, u'totalAssists': 10, u'totalDamageDealt': 158764, u'mostChampionKillsPerSession': 2, u'totalPentaKills': 0, u'mostSpellsCast': 0, u'totalDoubleKills': 0, u'maxChampionsKilled': 2, u'totalDeathsPerSession': 8, u'totalSessionsWon': 0, u'totalGoldEarned': 12405, u'totalTripleKills': 0, u'totalChampionKills': 2, u'maxNumDeaths': 8, u'totalMinionKills': 199, u'totalMagicDamageDealt': 5315, u'totalQuadraKills': 0, u'totalUnrealKills': 0, u'totalDamageTaken': 17519, u'totalSessionsLost': 1, u'totalFirstBlood': 0}, u'id': XX}, 2]}"
        summoner_id += "XX"

    parseSummonerStats(summoner_stats, summoner_id)

# Given the ranked stats, parse it to get the totalSessionsPlayed and
# corresponding champion id value
def parseSummonerStats(summoner_stats, summoner_id):
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

    sortChampions(summoner_id)

# Sort the list of all champions used by this summoner based on the number
# of totalSessionsPlayed (which is the first value in the pair)
def sortChampions(summoner_id):
    allChampionsUsed_sorted = sorted(allChampionsUsed, key=itemgetter(0))

    # Pass only the LAST pair to getChampionTitle (most used champion!)
    getChampionTitle(allChampionsUsed_sorted[-1], summoner_id)
    #print "Most used champ:" + str(allChampionsUsed_sorted[-1])

# Given a champion ID, look at the loChampionPairs file to get it's
# corresponding champion title
def getChampionTitle(mostUsedCHampionPair, summoner_id):
    # For every champion in loChampionPairs, get the most used champ's title
    for line in champions:
        line = line.split(' | ')
        if line[0] == mostUsedCHampionPair[1]:
            if summoner_id.__contains__("XX"):
                mostUsedChampion = "GAME DATA NOT FOUND"
            else:
                mostUsedChampion = line[1]
            #print "MOST USED CHAMPION FOR ID #" + str(summoner_id).strip("XX") +\
            #      " IS: " + str(mostUsedChampion)

            writeMostUsedChampion(summoner_id, mostUsedChampion)

# Write the most used champion back into Random_Summoners_1000.txt
def writeMostUsedChampion(summoner_id, mostUsedChampion):
    start = "'id': "
    end = ", '"

    lineCnt = 0

    # For every random summoner
    for line in random_summoners_1k:
        # Find the summoner ID
        result = re.search("%s(.*)%s" % (start, end), str(line)).group(1)

        # Once we've found the line where the passed in summoner id resides,
        if result == str(summoner_id).strip("XX"):
            # Strip out newlines so we can append most used champ at end,
            # append most used champion at end, then write newline back in.
            random_summoners_1k[lineCnt] = ''.join([line.strip('\n'),
                                           (" 'mostUsedChampion': " +
                                            str(mostUsedChampion) + " "), '\n'])

            # Write the new version of the line into the file
            with open('_out/Random_Summoners_run12.txt', 'w') as file:
                file.writelines(random_summoners_1k)

        lineCnt += 1

if __name__ == "__main__":
    main()