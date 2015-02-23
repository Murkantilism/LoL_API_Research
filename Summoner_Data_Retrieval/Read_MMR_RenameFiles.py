__author__ = 'Deniz'

import argparse, os

def main():

    parser = argparse.ArgumentParser(description='Attempt to search op.gg with the summoner names in every file in the'
                                                 'given directory location. Scrap html to find mmr and avg mmr.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    f = open(inputLocation, 'r')
    read_input = f.readlines()

    for line in read_input:
        split_line = line.split(":")
        print os.curdir+"\\"+split_line[0]
        print os.curdir+'\\'+split_line[1]
        os.rename(os.curdir+'\\'+split_line[0], os.curdir+'\\'+split_line[1])

if __name__ == "__main__":
    main()