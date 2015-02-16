__author__ = 'Deniz'

import time, subprocess, argparse, getopt
from sys import argv
import sys, os


DEFAULT_NUM_SUMMONERS = 250
DEFAULT_LOCATION = os.curdir + "\_out\Random_Summoners_run_"+str(time.time())

def main():
    parser = argparse.ArgumentParser(description='Attempt to generate X number'
                                                 ' of random summoners hourly.')

    parser.add_argument('-out', metavar='o', type=str, default=DEFAULT_LOCATION, help='the output location ' + str(DEFAULT_LOCATION))
    parser.add_argument('-num', metavar='n', type=int, default=DEFAULT_NUM_SUMMONERS,
                        help='number of summoners (default: ' +
                            str(DEFAULT_NUM_SUMMONERS) + ')',)

    args = parser.parse_args()

    #print vars(args).values()
    # Assign the number of summoners
    numSummoners = vars(args).values()[0]
    # Assign the output path
    outputLocation = vars(args).values()[1]

    subprocess.check_call('python Generate_Summoners.py' + ' -out ' +
                          str(outputLocation) + ' -num ' +
                          str(numSummoners), shell=True)
    subprocess.check_call('python Get_Most_Used_Champion.py' + ' -out ' +
                          str(outputLocation), shell=True)
    subprocess.check_call('python Check_Duplicate_Summoners.py' + ' -out ' +
                          str(outputLocation), shell=True)
    subprocess.check_call('python Scrub_Useless_Summoners.py' + ' -out ' +
                          str(outputLocation), shell=True)
    time.sleep(3600-time.time()%3600)
    main()

# The usage information returned when -h parameter is given
def usage():
    print "\nThis is the CLI for the dan audio matcher program\n"
    print 'Usage: ' + argv[0] + ' -f <set1> -f <set2>'

if __name__ == "__main__":
    main()