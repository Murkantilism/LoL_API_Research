__author__ = 'Deniz'

from RiotWatcher.riotwatcher import RiotWatcher
from RiotWatcher.riotwatcher import LoLException
import re
from random import randint

# Setup RiotWatcher object with api key
api = RiotWatcher('17dd8043-3e16-4cad-a388-985bfd93d275')

# A global counter used by Generate_Summoner_ID
cnt = 0

# The number of summoners we would like to generate
numSummoners = 5

def main():
    # Check if we have API calls remaining
    if(api.can_make_request()):
        me = api.get_summoner(None, '5908')
        #me = api.get_summoner(name='dyrus')
        #print(me)

        # Get summoner stats based on summoner object
        #my_ranked_stats = api.get_ranked_stats(me['id'])

        # Get league data based on summoner ID
        #my_league = api.get_league('5908')

        # Generate a bunch of random summoners
        while (cnt < numSummoners):
            Generate_Summoner_ID()

    print(api.can_make_request())

# Generate a random single summoner
def Generate_Summoner_ID():
    try:
        # Generate a random summoner ID between 4 to 7 digits
        random_id = random_with_N_digits(randint(4, 7))

        random_summoner = api.get_summoner(None, random_id)

        # Check if the summoner name is good
        # This is to avoid summoners like: IS148be5be2f2d180191298
        check_name = str(random_summoner).split("name': u'", 1)[1]

        if(check_name[0:3].__contains__("IS1")):
            print("Summoner ID " + str(random_id) + " has been culled (fake)")
        else:
            # Increment the counter if a real summoner is found
            global cnt;
            cnt = cnt + 1

            print "Summoner ID " + str(random_id) + " Exists!"

            # Write the summoner to a text doc
            Write_Summoner(random_summoner)

    # If the random summoner ID isn't a real summoner, catch error
    except LoLException:
        print "Summoner ID " + str(random_id) + " Does Not Exist"

# Helper method to create random numbers of a certain digit length
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# Write this summoner to a text document
def Write_Summoner(summoner):
    # Write a newline after each } to make output readable
    summoner = re.sub(r'([}])', r'}\n', str(summoner))

    # Cull all extraneous u' characters (leaving ' character)
    summoner = re.sub(r"([u]+['])", r"'", str(summoner))

    f = open('Random_Summoners.txt', 'a')
    f.write(str(summoner))
    f.close()

# Method to write a readable text file of the *crapton* of league data returned
def Write_League_Data(_id):
    my_league = api.get_league(_id)
    # Write a newline after each } to make output readable
    my_league = re.sub(r'([}])', r'}\n', str(my_league))

    # Cull all extraneous u' characters (leaving ' character)
    my_league = re.sub(r"([u]+['])", r"'", str(my_league))

    f = open('Leage_Data', 'w')
    f.write(str(my_league))
    f.close()

if __name__ == "__main__":
    main()