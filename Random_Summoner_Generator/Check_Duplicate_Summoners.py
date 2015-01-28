__author__ = 'Deniz'

import re, argparse

# Declare an empty list of summoners
lo_summoners = []
lo_ids = []
no_dups_lo_summoners = []
def main():

    # Command line parsing
    global outputLocation

    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners.')

    parser.add_argument('-out', metavar='o', type=str)

    args = parser.parse_args()

    print vars(args).values()
    #outputLocation = '_out/Compiled_Summoners_1000'
    outputLocation = vars(args).values()[0]


    global lo_summoners
    global lo_ids
    global no_dups_lo_summoners
    f = open(outputLocation+".txt", 'r')
    read_lines = f.readlines()

    duplicate_cnt = 0

    start = "'id': "
    end = ", 'name': '"

    # For every line in the file, get the summoner ID
    for line in read_lines:
        result = re.search("%s(.*)%s" % (start, end), str(line)).group(1)
        lo_ids.append(result)

    duplicate_ids = []
    seen_ids = []
    # Get all the duplicate IDs
    for id in lo_ids:
        if id not in seen_ids:
            seen_ids.append(id)
        else:
            duplicate_ids.append(id)

    duplicate_summoners = []
    # For every line
    for line in read_lines:
        # Get this line's ID
        result = re.search("%s(.*)%s" % (start, end), str(line)).group(1)

        # Check if the ID is a duplicate, if so add it to list of dups
        if result in duplicate_ids:
            duplicate_summoners.append(line)
            duplicate_cnt += 1
        # Otherwise add it to non-duplicate list
        else:
            no_dups_lo_summoners.append(line)

    # Write the duplicates to a separate text file
    g = open(outputLocation+"_DUPLICATES.txt", 'a')
    for summoner in duplicate_summoners:
        g.write(summoner)

    # Write the non-duplicates to main file
    f = open(outputLocation+".txt", 'a')
    f.write("===============================================================\n")
    for summoner in no_dups_lo_summoners:
        f.write(summoner)

    print str(duplicate_cnt) + ' DUPLICATE SUMMONERS DELETED'

    f.close()

if __name__ == "__main__":
    main()