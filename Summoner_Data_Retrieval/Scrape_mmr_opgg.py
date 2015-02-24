__author__ = 'Deniz'

from bs4 import BeautifulSoup
from splinter import Browser
import argparse, os, re, time

mmr_filepath_Dict = {}
def main():
    global mmr_filepath_Dict
    BASE_URL = "http://na.op.gg/"

    parser = argparse.ArgumentParser(description='Attempt to search op.gg with the summoner names in every file in the'
                                                 'given directory location. Scrap html to find mmr and avg mmr.')

    parser.add_argument('-in', metavar='i', type=str)

    args = parser.parse_args()

    inputLocation = vars(args).values()[0]

    get_summoner_ids_names(inputLocation, BASE_URL)

# For every file in the input dir, get the summoner names and ids
def get_summoner_ids_names(inputLocation, BASE_URL):
    # Define search terms for summoner id
    start_summoner_id = "': "
    end_summoner_id = ", u'matchHistoryUri"

    # Define search terms for summoner name
    start_summoner_name = "u'summonerName': u'"
    end_summoner_name = "'}"


    for root, __, files in os.walk(inputLocation):
        for f in files:
            fullpath = os.path.join(root, f)
            f = open(fullpath, 'r')
            read_file = f.readlines()
            f.close()
            # Split up the match history (which is all 1 line) by the summonerId string
            match_history_split = str(read_file).split("u'summonerId")
            # Pop off first element of array (doesn't contain any summoner ID's)
            match_history_split.pop(0)
            #print match_history_split[0]

            # Get first element of array
            match = match_history_split[0]
            # Lop off everything past 135 characters
            match = match[:135]
            #print "MATCH: " + match

            # Find the summoner id
            tmp_id = re.search("%s(.*)%s" % (start_summoner_id, end_summoner_id), str(match)).group(1)
            # Find the summoner name
            tmp_name = re.search("%s(.*)%s" % (start_summoner_name, end_summoner_name), str(match)).group(1)
            # Strip the summoner name of all whitespace
            tmp_name = tmp_name.replace(' ', '')

            # Pass the name, id to splinter to search on op.gg
            browser = navigate_to_summoner_page(BASE_URL, tmp_name)
            # Attempt to click Check MMR button
            click_check_mmr(browser, fullpath, tmp_name)
            # Parse the webpage to find mmr
            find_mmr(browser, fullpath, tmp_name)


def navigate_to_summoner_page(BASE_URL, summonerName):
    browser = Browser('chrome')
    print "BROWSER visiting URL: " + str(BASE_URL+'summoner/userName='+summonerName)
    browser.visit(BASE_URL+'summoner/userName='+summonerName)
    return browser

def click_check_mmr(browser, fullpath, summonerName):
    # Declare boolean switch
    summonerFound = False
    # Find the second button with the css .opButton.small (the first button is Ingame Info, second is Check MMR)
    try:
        button = browser.find_by_css('.opButton.small')[1]
        button.click()
        summonerFound = True
    except Exception:
        summonerFound = False
        print "ERR: Summoner " + summonerName + " NOT found."

    if summonerFound:
        # Parse the webpage to find mmr
        find_mmr(browser, fullpath, summonerName)

# Declare attempt counter
atmpt_cnt = 0
def find_mmr(browser, fullpath, summonerName):
    global atmpt_cnt
    # Wait 2 seconds before searching for MMR data
    time.sleep(2)
    # Declare boolean switch
    mmr_found = False

    # Find the MMR by css
    try:
        get_mmr = browser.find_by_css('div.InnerSummonerMMR').first.value
        mmr_found = True
    except Exception:
        if atmpt_cnt < 5:
            print "ERR: MMR CSS NOT FOUND"
            print "ATTEMPT " + str(atmpt_cnt) + ": Waiting 5 seconds before trying again..."
            time.sleep(5)
            atmpt_cnt += 1
            mmr_found = False
            # Recursively try to click MMR button and parse again, up to 5 times.
            click_check_mmr(browser, fullpath, summonerName)
        else:
            mmr_found = False
            print "ERR: MMR CSS NOT FOUND, ALL ATTEMPTS EXHAUSTED"

    if mmr_found:
        # Define search terms
        start = 'MMR for this league is '
        end = 'beta'
        # Define regex to search for mmr
        mmr = re.findall("%s(.*)%s" % (start, end), str(get_mmr), re.S)

        # Split mmr to get avg mmr and mmr
        mmr = str(mmr).split(r'.\n')

        try:
            # Strip last 2 characters off avg mmr ']
            mmr[0] = mmr[0][2:]
            _avg_mmr = mmr[0]
        except IndexError:
            # This means avg mmr wasn't found properly
            print 'ERR: AVG MMR NOT FOUND PROPERLY'
            _avg_mmr = 'NONE'
        try:
            # Strip first 2 characters off mmr ['
            mmr[1] = mmr[1][:-2]
            _mmr = mmr[1]
        except IndexError:
            # This means mmr wasn't found properly
            print 'ERR: MMR NOT FOUND PROPERLY'
            _mmr = 'NONE'

        print "MMR: " + _mmr
        print "AVERAGE LEAGUE MMR: " + _avg_mmr

        atmpt_cnt = 0  # Reset attempt counter

        # Close the browser, kills chromedriver.exe as well
        browser.quit()

        # Write MMR info to filenames
        write_mmr(_avg_mmr, _mmr, fullpath)

# Given avg mmr, mmr, and a filepath slice the last 4 characters off the filepath (.txt) append
# the avg mmr and mmr, add .txt back in and replace the old filepath with the new one.
def write_mmr(avg_mmr, mmr, fullpath):
    # Rename the file
    os.rename(os.curdir+'\\'+fullpath, os.curdir+'\\'+fullpath[:-4]+"_mmr="+str(mmr)+"_avg="+str(avg_mmr)+'.txt')


if __name__ == "__main__":
    main()