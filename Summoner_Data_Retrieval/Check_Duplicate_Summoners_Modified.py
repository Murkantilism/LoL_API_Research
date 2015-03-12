__author__ = 'Deniz'

import argparse

def main():

    # Command line parsing
    global inputLocation

    parser = argparse.ArgumentParser(description='Remove duplicate summoners.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    print vars(args).values()
    inputLocation = vars(args).values()[0]

    lo_summoners = []

    f = open(inputLocation, 'r')
    read_lines = f.readlines()

    # For every line in the file, append it to an array
    for line in read_lines:
        lo_summoners.append(line)

    # Convert array to a set and back to array to remove dups (thanks Python!)
    lo_summoners_noDups = list(set(lo_summoners))

    # Write the non-duplicates to output
    f = open(inputLocation, 'w')
    for summoner in lo_summoners_noDups:
        f.write(summoner)

    print str(len(lo_summoners) - len(lo_summoners_noDups)) + ' DUPLICATE SUMMONERS DELETED'

    f.close()

if __name__ == "__main__":
    main()