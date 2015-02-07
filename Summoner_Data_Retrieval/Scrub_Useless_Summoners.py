__author__ = 'Deniz'

import argparse

# Declare an empty list of summoners
lo_summoners = []
def main():

    # Command line parsing
    global outputLocation

    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners.')

    parser.add_argument('-out', metavar='o', type=str)

    args = parser.parse_args()

    print vars(args).values()
    outputLocation = vars(args).values()[0]

    global lo_summoners
    f = open(outputLocation+'.txt', 'r')
    champions = f.read()
    champions = champions.splitlines()

    scrubCnt = 0

    cnt = 0

    # For every line in the file, if the most used
    # champ is "GAME DATA NOT FOUND", erase it
    for line in champions:
        try:
            if str(line.split("'mostUsedChampion': ", 1)[1]).__contains__("GAME DATA NOT FOUND"):
                champions[cnt] = ''  # Erase that summoner line
                scrubCnt += 1
            else:
                champions[cnt] += "\n"
        except IndexError:
            "Most used champion not found"
            champions[cnt] = ''  # Erase that summoner line
            scrubCnt += 1

        cnt += 1


    # Close file and reopen in write mode (to overwrite it)
    #f.close()
    f = open(outputLocation+'.txt', 'w')

    # Write the new list sans duplicates
    for summoner in champions:
        f.write(summoner)

    print str(scrubCnt) + ' SUMMONERS WITH NO DATA SCRUBBED'

    f.close()

if __name__ == "__main__":
    main()