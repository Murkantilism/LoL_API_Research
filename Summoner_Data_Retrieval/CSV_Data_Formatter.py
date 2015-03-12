__author__ = 'Deniz'

import argparse, csv, os, re
from collections import OrderedDict

summoner_match_history_arryOfDicts = []
def main():
    global summoner_match_history

    parser = argparse.ArgumentParser(description='Parse input directory and write summoner data to CSV file.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    # Loop through every file in the given input dir
    for root, __, files in os.walk(inputLocation):
        for f in files:
            fullpath = os.path.join(root, f)
            parse_input(fullpath, f)
            get_mmr(f)
            write_csv(f)


# Given an input filepath, read and parse the summoner data into a dict
def parse_input(filepath, filename):
    # Read input file
    f = open(filepath, 'r')
    read_file = f.read()
    f.close()
    # Split the file into each match
    split_file = read_file.split("u'matchId': ")

    # Define search terms
    start = ", u'"
    end = ", u'"


    # Save the match history info like matchId, mapId,
    match_history_header = split_file[0]

    # Wipe the array of dicts
    summoner_match_history_arryOfDicts[:] = []

    # For every match find the field and it's value, add them to dict
    for match in split_file:
        # Split based on commas
        split_match = match.split(',')
        # Pop off the first element RANKED_TEAM_5x5 we don't care about
        split_match.pop(0)

        # Declare temp dict
        tmp_dict = OrderedDict()



        for field in split_match:
            # Strip out all unneeded characters
            field = field.replace('participants:', '')
            field = field.replace('stats:', '')
            field = field.replace('{', '')
            field = field.replace('}', '')
            field = field.replace('[', '')
            field = field.replace(']', '')
            field = field.replace(" u'", '')
            field = field.replace("u'", '')
            field = field.replace("'", '')

            # If the field is empty (due to above characters being stripped) skip it
            if ' ' == field:
                pass
            # Otherwise, split this field based on : to get key and value for dict
            else:
                split_field = field.split(":")
                # Remove any spaces from the value
                split_field[1] = split_field[1].replace(' ', '')
                # Populate the tmp dict with fields
                tmp_dict[split_field[0]] = split_field[1]

        if len(tmp_dict.keys()) > 0:
            # Get the MMR and AVG mmr keys and values
            mmr_k, mmr_v = get_mmr(filename=filename)
            avg_mmr_k, avg_mmr_v = get_avg_mmr(filename=filename)
            # Append them at the end of the tmp dict
            tmp_dict[mmr_k] = mmr_v
            tmp_dict[avg_mmr_k] = avg_mmr_v
            # Append tmp dict to the array of dicts
            summoner_match_history_arryOfDicts.append(tmp_dict)


def get_mmr(filename):
    # Lop off everything before the last 23 characters (mmr info) and
    # then lop off last 4 characters (.txt)
    mmr_info = filename[-23:-4]
    # Split mmr info by  underscore
    mmr_info = mmr_info.split('_')

    # MMR is element 0 of split array
    mmr = mmr_info[0]

    # Strip comma out of value
    mmr = mmr.replace(',', '')

    # MMR label is first 3 characters of mmr element, actual MMR value is everything but first 4 characters (mmr=)
    return mmr[:3], mmr[4:]


def get_avg_mmr(filename):
    # Lop off everything before the last 23 characters (mmr info) and
    # then lop off last 4 characters (.txt)
    mmr_info = filename[-23:-4]
    # Split mmr info by  underscore
    mmr_info = mmr_info.split('_')

    # Avg MMR is element 1 of split array
    avg_mmr = mmr_info[1]

    # Strip comma out of value
    avg_mmr = avg_mmr.replace(',', '')

    # Avg label is first 3 characters of avg mmr element, actual Avg value is everything but first 4 characters (avg=)
    return avg_mmr[:3], avg_mmr[4:]


def write_csv(filename):

    #for dictionary in summoner_match_history_arryOfDicts:
    #    for k, v in dictionary.iteritems():
    #        print str(k) + " : " + str(v)

    # Pop the first empty dict from array of dicts
    summoner_match_history_arryOfDicts.pop(0)

    # Open CSV file at output folder + filename minus _mmr=x,xxx_avg=x,xxx.txt + .csv
    with open('.\_outMatchHistoryCSV_0to15\\'+filename[:-4]+'.csv', 'a') as csvfile:
        # Assign fieldnames (headers)
        fieldnames = summoner_match_history_arryOfDicts[0].keys()
        print len(fieldnames)
        print len(summoner_match_history_arryOfDicts)
        # Create CSV writer object
        writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_NONE, fieldnames=fieldnames, extrasaction='ignore')
        # Write headers
        writer.writeheader()
        # Every every dict in the array of dicts, write it as a row
        for dictionary in summoner_match_history_arryOfDicts:
            writer.writerow(dictionary)

if __name__ == "__main__":
    main()