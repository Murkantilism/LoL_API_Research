__author__ = 'Deniz'

import argparse, os, os.path

input_dir0_filenames = []
input_dir1_filenames = []
unlike_filenames = []
def main():
    global input_dir0_filenames
    global input_dir1_filenames
    global unlike_filenames

    parser = argparse.ArgumentParser(description="Given dir0 and dir1 locations, search for files in dir0 that "
                                                 "don't have the same corresponding filename in dir1")

    parser.add_argument('-dir0', metavar='d0', type=str)
    parser.add_argument('-dir1', metavar='d1', type=str)

    args = parser.parse_args()

    dir0 = vars(args).values()[1]
    dir1 = vars(args).values()[0]

    read_filenames(dir0, dir1)
    find_unlike_filenames(dir0, dir1)


# Read the filename of every file in each input directory, store in array
def read_filenames(dir0, dir1):
    for root, __, files in os.walk(dir0):
        for f in files:
            fullpath = os.path.join(root, f)
            #print fullpath
            input_dir0_filenames.append(fullpath)

    for root, __, files in os.walk(dir1):
        for f in files:
            fullpath = os.path.join(root, f)
            #print fullpath
            input_dir1_filenames.append(fullpath)

# Search for files in dir0 that don't have the same corresponding filename in dir1
def find_unlike_filenames(dir0, dir1):
    fileFound = False  # Declare boolean flag
    cnt = 0  #  Declare counter
    # First loop through every filename in dir0 and compare against every filename in dir1
    for filename in input_dir0_filenames:
        fileFound = False
        cnt = 0
        #for filename1 in input_dir1_filenames:
        while fileFound == False:
            try:
                #print str(filename)[25:] + " == " + str(input_dir1_filenames[cnt])[26:]
                #print input_dir1_filenames[cnt] == input_dir1_filenames[-1]
                # If filenames are the same, we've found are match and can
                # stop inner loop temporarily
                if str(filename)[25:] == str(input_dir1_filenames[cnt])[26:]:
                    fileFound = True
                # Otherwise check if this is the last file of dir1. If it is
                # this must be an unlike file.
                elif(input_dir1_filenames[cnt] == input_dir1_filenames[-1]):
                    print "UNLIKE FILE FOUND: ./dir0/" + filename[25:]
                    #unlike_filenames.append(filename[25:])
                    os.remove(dir0+'/'+(filename[25:]))
                # Otherwise pass and continue inner loop
                else:
                    pass
                cnt += 1
            except IndexError:
                fileFound = True

    # Next loop through every filename in dir1 and compare against every filename in dir0
    for filename in input_dir1_filenames:
        fileFound = False
        cnt = 0
        while fileFound == False:
            try:
                #print str(filename)[26:] + " == " + str(input_dir0_filenames[cnt])[25:]
                #print input_dir0_filenames[cnt] == input_dir0_filenames[-1]
                # If filenames are the same, we've found are match and can
                # stop inner loop temporarily
                if str(filename)[26:] == str(input_dir0_filenames[cnt])[25:]:
                    fileFound = True
                # Otherwise check if this is the last file of dir1. If it is
                # this must be an unlike file.
                elif(input_dir0_filenames[cnt] == input_dir0_filenames[-1]):
                    print "UNLIKE FILE FOUND: ./dir1/" + filename[26:]
                    #unlike_filenames.append(filename[26:])
                    os.remove(dir1+'/'+(filename[26:]))
                # Otherwise pass and continue inner loop
                else:
                    pass
                cnt += 1
            except IndexError:
                fileFound = True

# Given an array of unlike filenames, delete those files
def delete_unlike_files():
    return



if __name__ == "__main__":
    main()