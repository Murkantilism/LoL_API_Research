__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException

# Setup RiotWatcher object with api key
api = RiotWatcher('17dd8043-3e16-4cad-a388-985bfd93d275')

def main():
    # Check if we have API calls remaining
    if(api.can_make_request()):
        summoner_stats = api.get_ranked_stats(summoner_id="86413", region=None, season=None)
        f = open('Summoner_Stats.txt', 'a')
        f.write(str(summoner_stats))


        # Keyword: u'id':  tells us the champion ID

        f.write("\n\n\n")

        game = api.get_recent_games(summoner_id="86413", region=None)
        f.write(str(summoner_stats))
        f.close()

# Get the ranked stats of the given summoner
def getSummonerStats():


    parseSummonerStats()

# Given the ranked stats, parse it to get the totalSessionsPlayed and
# corresponding champion id value
def parseSummonerStats():

    getChampionTitle()

# Given a champion ID, look at the loChampionPairs file to get it's
# corresponding champion title
def getChampionTitle():
    f = open('loChampionPairs', 'r')
    champions = f.read()



if __name__ == "__main__":
    main()