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
champions = champions.split('\n')

with open('_out/Random_Summoners_1000.txt', 'r') as file:
    # read a list of lines into data
    random_summoners_1k = file.readlines()

def main():
    # Check if we have API calls remaining
    if(api.can_make_request()):
        getSummoners()

        #summoner_stats = api.get_ranked_stats(summoner_id="86413", region=None, season=None)
        #f = open('Summoner_Stats.txt', 'a')
        #f.write(str(summoner_stats))

        #f.write("\n\n\n")

        #game = api.get_recent_games(summoner_id="86413", region=None)
        #f.write(str(summoner_stats))
        #f.close()


        # Keyword: u'id':
        # Keyword: u'totalSessionsPlayed':

def getSummoners():
    f = open('_out/Random_Summoners_1000.txt', 'r')
    summoners = f.read()
    summoners = summoners.split('\n')

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
        parseSummonerStats(summoner_stats, summoner_id)
    except LoLException:
        print "GAME DATA NOT FOUND FOR SUMMONER: " + str(summoner_id)

# Given the ranked stats, parse it to get the totalSessionsPlayed and
# corresponding champion id value
def parseSummonerStats(summoner_stats, summoner_id):
    summoner_stats = str(summoner_stats).split(', {')

    start = "'totalSessionsPlayed': "
    end = ", u'totalAssists"

    start1 = "u'id': "
    end1 = "}"

    for s in summoner_stats:
        #print str(s) + "\n"
        # Get the number of totalSessionsPlayed
        result = re.search("%s(.*)%s" % (start, end), str(s)).group(1)
        # And the corresponding champion
        result1 = re.search("%s(.*)%s" % (start1, end1), str(s)).group(1)
        # And create a pair [totalSessionsPlayed, id]
        #print 'RESULT: ' + str(result) + '\n'
        #print 'RESULT ONE: ' + str(result) + '\n'
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
            #print str(line[0]) + "|" + str(mostUsedCHampionPair[1])
            mostUsedChampion = line[1]
            print "MOST USED CHAMPION FOR ID: " + str(summoner_id) +\
                  " IS : " + str(mostUsedChampion)
            writeMostUsedChampion(summoner_id, mostUsedChampion)

def writeMostUsedChampion(summoner_id, mostUsedChampion):
    start = "'id': "
    end = ", '"

    lineCnt = -1

    # For every random summoner
    for line in random_summoners_1k:
        lineCnt += 1
        # Find the summoner ID
        result = re.search("%s(.*)%s" % (start, end), str(line)).group(1)

        # Once we've found the line where the passed in summoner id resides,
        if result == summoner_id:
            print 'RESULT: ' + str(result) + ' SUMMONER ID: ' +\
                  str(summoner_id)

            # Append the most used champion at the end of the line

            print random_summoners_1k[lineCnt]
			
			# Strip out the newlines so we can append most used champ at the end
            line.rstrip('\n')
			# Append most used champion at the end FIXME: Still isn't appending at the end of line
            random_summoners_1k[lineCnt] += "'mostUsedChampion': " +\
                                            str(mostUsedChampion) + " "
            # Write the newline back in
            random_summoners_1k[lineCnt] += '\n' # FIXME: perhaps this is the problem?

            # Write the new version of the line into the file
            with open('_out/Random_Summoners_1000.txt', 'w') as file:
                file.writelines(random_summoners_1k)


if __name__ == "__main__":
    main()