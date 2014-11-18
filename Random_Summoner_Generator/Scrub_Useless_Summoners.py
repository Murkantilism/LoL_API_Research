__author__ = 'Deniz'

# Declare an empty list of summoners
lo_summoners = []
def main():
    global lo_summoners
    f = open('_out/Random_Summoners_run5.txt', 'r')
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
    f = open('_out/Random_Summoners_run5.txt', 'w')

    # Write the new list sans duplicates
    for summoner in champions:
        f.write(summoner)

    print str(scrubCnt) + ' SUMMONERS WITH NO DATA SCRUBBED'

    f.close()

if __name__ == "__main__":
    main()