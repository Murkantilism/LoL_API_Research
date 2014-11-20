__author__ = 'Deniz'

import re

# Declare an empty list of summoners
lo_summoners = []
lo_ids = []
duplicate_summoners = []
final_lo_summoners = []
def main():
    global lo_summoners
    global lo_ids
    global final_lo_summoners
    f = open('_out/Random_Summoners_run0_run12_370.txt', 'r')
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

    '''
    # For every ID, add the non-duplicate summoners to final list
    for id in duplicate_ids:
        for line in read_lines:
            # Get the ID of this line
            line_id = re.search("%s(.*)%s" % (start, end), str(line)).group(1)

             # If the ID is not in the list of duplicates, add to final list
            if not(str(line_id) == str(id)):
                final_lo_summoners.append(line)
    '''

    occurrenceCnt = 0  # Declare occurance counter
    # For every ID, check if it's got a duplicate ID
    for id in duplicate_ids:
        for line in read_lines:
            # Get the ID of this line
            line_id = re.search("%s(.*)%s" % (start, end), str(line)).group(1)

            # If the ID is in the list of dups, SAVE first occurrence then
            # forget the rest of the occurrences
            if str(line_id) == str(id):
                if occurrenceCnt == 0:
                    occurrenceCnt += 1
                    #final_lo_summoners.append(line)
                else:
                    duplicate_cnt += 1
                    duplicate_summoners.append(line)

        occurrenceCnt = 0  # Reset occurrence counter when we try next ID

    f = open('_out/Random_Summoners_run0_run12_370.txt', 'w')

    # Write the final list
    for summoner in final_lo_summoners:
        f.write(summoner)

    print str(duplicate_cnt) + ' DUPLICATE SUMMONERS DELETED'

    f.close()

if __name__ == "__main__":
    main()