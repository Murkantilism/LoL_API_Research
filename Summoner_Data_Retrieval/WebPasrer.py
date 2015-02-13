__author__ = 'Deniz'
import argparse, re, os

def main():
    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    summoner_name_parse_pass0(inputLocation)
    summoner_name_parse_pass1(inputLocation)


# Given an input file, read and parse for the summoner names
def summoner_name_parse_pass0(inputLocation):
    # Read input txt file
    f = open(inputLocation, 'r')
    lines = f.readlines()

    # Search for summoner string after <a href="http://www.mobafire.com/profile/    and before hyphen
    start = '<a href="http://www.mobafire.com/profile/'
    end = '" class="'

    array_summoners = []  # Keep an array of summoners, write it at the end
    lineNum = 0           # Count the total number of lines read
    summonerFoundNum = 0       # Count number of summoners found

    for line in lines:
        lineNum += 1
        try:
            summoner_name = re.search("%s(.*)%s" % (start, end), str(line)).group(1)
            summonerFoundNum += 1
            array_summoners.append(summoner_name[:-7])  # Lop off the last 7 digit of the string,
                                                        # contains useless hyphen and random digits
            #print "Summoner found in line " + str(lineNum)
        except AttributeError:
            pass
            # print "No summoner in line " + str(lineNum)

    print "OUT: " + str(lineNum) + " lines parsed, " + str(summonerFoundNum) + " summoners found."
    file = open(os.curdir+"\_outSummonerParser\summonerParserOutput"+inputLocation+".txt", 'w')
    for summoner in array_summoners:
        file.writelines(str(summoner)+"\n")

def summoner_name_parse_pass1(inputLocation):
    # Read input txt file
    f = open(inputLocation, 'r')
    lines = f.readlines()

    # Search for summoner string after <a href="http://www.mobafire.com/profile/    and before hyphen
    start = '<a href="/profile/'
    end = '" class="'

    array_summoners = []  # Keep an array of summoners, write it at the end
    lineNum = 0           # Count the total number of lines read
    summonerFoundNum = 0       # Count number of summoners found

    for line in lines:
        lineNum += 1
        try:
            summoner_name = re.search("%s(.*)%s" % (start, end), str(line)).group(1)
            summonerFoundNum += 1
            array_summoners.append(summoner_name[:-7])  # Lop off the last 7 digit of the string,
                                                        # contains useless hyphen and random digits
            #print "Summoner found in line " + str(lineNum)
        except AttributeError:
            pass
            # print "No summoner in line " + str(lineNum)

    print "OUT: " + str(lineNum) + " lines parsed, " + str(summonerFoundNum) + " summoners found."
    file = open(os.curdir+"\_outSummonerParser\summonerParserOutput"+inputLocation+".txt", 'w')
    for summoner in array_summoners:
        file.writelines(str(summoner)+"\n")

if __name__ == "__main__":
    main()