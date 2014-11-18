__author__ = 'Deniz'

# Declare an empty list of summoners
lo_summoners = []
def main():
    global lo_summoners
    f = open('_out/Random_Summoners_run5.txt', 'r')

    origCnt = 0
    newCnt = 0

    # For every line in the file
    for line in f:
        # Append each line of summoners into a list
        lo_summoners.append(str(line))
        origCnt += 1

    # Convert the list of summoners to a set. then back to a
    # list to cull duplicates (does not preserve order, don't need to)
    noDuplicates_lo_summoners = list(set(lo_summoners))

    # Close file and reopen in write mode (to overwrite it)
    #f.close()
    f = open('_out/Random_Summoners_run5.txt', 'w')

    # Write the new list sans duplicates
    for summoner in noDuplicates_lo_summoners:
        f.write(summoner)
        newCnt += 1

    print str(origCnt - newCnt) + ' DUPLICATE SUMMONERS DELETED'

    f.close()

if __name__ == "__main__":
    main()

# Search for "'id': " keyword, take everything after, which includes:
# the summoner id and summoner name
#summoner_id = line.split("'id': ",1)[1]

# Test duplicates subjects:
# sleepymanny  Jascari
# GoSoO        pheonixfenix