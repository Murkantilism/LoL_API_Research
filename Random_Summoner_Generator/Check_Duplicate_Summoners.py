__author__ = 'Deniz'
# Declare an empty list of summoners
lo_summoners = []
def main():
    global lo_summoners
    f = open('Random_Summoners_1000.txt', 'r')
    #f.read()
    print(str(f))

    # For every line in the file
    for line in f:
        # Append each line of summoners into a list
        lo_summoners.append(str(line))
        print str(line)

    # Convert the list of summoners to a set. then back to a
    # list to cull duplicates (does not preserver order)
    #noDuplicates_lo_summoners = set()
    #any(x in noDuplicates_lo_summoners or noDuplicates_lo_summoners.add(x) for x in lo_summoners)
    noDuplicates_lo_summoners = list(set(lo_summoners))

    # Close file and reopen in write mode (to overwrite it)
    #f.close()
    f = open('Random_Summoners_1000.txt', 'w')

    # Write the new list sans duplicates
    for summoner in noDuplicates_lo_summoners:
        f.write(summoner)

    f.close()

#def remove_dups():


if __name__ == "__main__":
    main()

# Search for "'id': " keyword, take everything after, which includes:
# the summoner id and summoner name
#summoner_id = line.split("'id': ",1)[1]

# Test subjects:
# sleepymanny  Jascari
# GoSoO        pheonixfenix