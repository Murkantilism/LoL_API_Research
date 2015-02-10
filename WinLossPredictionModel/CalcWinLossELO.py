__author__ = 'Deniz'

import re, argparse



def main():

    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    calcWinLoss(inputLocation)

# Given a txt file with 15 games worth of match history, calc win loss percentage
def calcWinLoss(inputLocation):
    # Read txt file
    f = open(inputLocation, 'r')
    lines = f.readline()

    # Search for true/false value after u'winner': field
    start = "u'winner': "
    end = ", u'"

    numWins = 0
    numLosses = 0

    for line in lines:
        winner = re.search("%s(.*)%s" % (start, end), str(line)).group(1)

        if winner == "True":
            numWins += 1
        elif winner == "False":
            numLosses += 1

    netWins = numWins - numLosses
    winPercentage = (netWins / 15) * 100
    return winPercentage

# Given the ELO rating of two players, calculate the expected outcome using:
# 1 / 1 + 10^((rb - ra) / 400)
def calcExpectedOutcome(ra, rb):
    expectedOutcome = 1 / (1 + 10**((rb - ra)/400))
    return expectedOutcome

if __name__ == "__main__":
    main()