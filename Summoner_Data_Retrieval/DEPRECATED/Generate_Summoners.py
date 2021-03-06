__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re, argparse
from random import randint
import subprocess

# Setup RiotWatcher object with api key
f = open('apikey.txt', 'r')
api = RiotWatcher(f.read())

# A global counter used by Generate_Summoner_ID
cnt = 0

numSummonersWritten = 0
def main():

    # Command line parsing
    global outputLocation

    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners.')

    parser.add_argument('-out', metavar='o', type=str)
    parser.add_argument('-num', metavar='n', type=int)

    args = parser.parse_args()

    print vars(args).values()
    numSummoners = vars(args).values()[0]
    outputLocation = vars(args).values()[1]

    # Check if we have API calls remaining
    if(api.can_make_request()):
        # Generate a bunch of random summoners
        while (cnt < numSummoners):
            Generate_Summoner_ID()

        print str(numSummonersWritten) + " SUMMONERS GENERATED"

# Generate a random single summoner
def Generate_Summoner_ID():
    try:
        # Generate a random summoner ID between 4 to 7 digits
        random_id = random_with_N_digits(randint(4, 7))

        random_summoner = api.get_summoner(None, random_id)

        # Check if the summoner exists
        if Check_Summoner(random_id, random_summoner):
            #print "Summoner Exists"
            # Check the summoner's level
            if Check_Level(random_id) == True:
                #print "Level checked"
                # Check the summoner's ranking
                if Check_Rank(random_id) == True:
                    print "Rank checked"
                    # Write the summoner to a text doc
                    Write_Summoner(random_summoner)


    # If the random summoner ID isn't a real summoner, catch error
    except LoLException:
        print "Summoner ID " + str(random_id) + " Does Not Exist"
        return

# Helper method to create random numbers of a certain digit length
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# Check if the summoner name is good
# This is to avoid summoners like: IS148be5be2f2d180191298
def Check_Summoner(random_id, random_summoner):
    check_name = str(random_summoner).split("name': u'", 1)[1]

    if(check_name[0:3].__contains__("IS1")):
        print("Summoner ID " + str(random_id) + " has been culled (fake)")
        return False
    else:
        # Increment the counter if a real summoner is found
        global cnt
        cnt = cnt + 1

        print "Summoner ID " + str(random_id) + " Exists!"

        return True

def Check_Level(random_id):
    check_level = api.get_summoner(name=None, id=random_id, region=None)

    start = "u'summonerLevel': "
    end = ", u'revisionDate"

    result = re.search("%s(.*)%s" % (start, end), str(check_level)).group(1)

    if (str(result) == "30"):
        return True
    else:
        return False

# Checks if the given summoner ID is in Gold or Platinum
def Check_Rank(random_id):
    try:
        check_rank = api.get_league_entry(str(random_id), team_ids=None, region=None)
    except LoLException:
        print "Summoner ID " + str(random_id) + " is not in any league"
        return

    # Only check the first 40 characters (in case GOLD is in username/elsewhere)
    if str(check_rank)[0:40].__contains__("GOLD") | \
       str(check_rank)[0:40].__contains__("PLATINUM"):
        print "RANK: " + str(check_rank)
        return True
    else:
        print("Summoner ID " + str(random_id) + " is not in GOLD or PLATINUM")
        return False

# Write this summoner to a text document
def Write_Summoner(summoner):
    # Write a newline after each } to make output readable
    summoner = re.sub(r'([}])', r'}\n', str(summoner))

    # Cull all extraneous u' characters (leaving ' character)
    summoner = re.sub(r"([u]+['])", r"'", str(summoner))

    f = open(outputLocation+".txt", 'a')
    f.write(str(summoner))
    global numSummonersWritten
    numSummonersWritten = numSummonersWritten + 1
    f.close()

# Method to write a readable text file of the *crapton* of league data returned
def Write_League_Data(_id):
    my_league = api.get_league(_id)
    # Write a newline after each } to make output readable
    my_league = re.sub(r'([}])', r'}\n', str(my_league))

    # Cull all extraneous u' characters (leaving ' character)
    my_league = re.sub(r"([u]+['])", r"'", str(my_league))

    f = open('League_Data', 'w')
    f.write(str(my_league))
    f.close()

if __name__ == "__main__":
    main()