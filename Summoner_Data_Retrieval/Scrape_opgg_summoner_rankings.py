__author__ = 'Deniz'

from bs4 import BeautifulSoup
from splinter import Browser
import argparse, os, re, time, sys

mmr_filepath_Dict = {}
def main():
    global mmr_filepath_Dict
    BASE_URL = "http://na.op.gg/ranking/ladder/"

    parser = argparse.ArgumentParser(description='Attempt to scrape op.gg rankings to get X number of summoner names '
                                                 'in gold and plat.')

    parser.add_argument('-numSum', metavar='n', type=str)

    args = parser.parse_args()

    numSummoners = vars(args).values()[0]


    #get_summoner_ids_names(inputLocation, BASE_URL)
    navigate_to_platgold_rankings_page(BASE_URL, numSummoners)

def navigate_to_platgold_rankings_page(BASE_URL, numSummoners):
    browser = Browser('chrome')
    print "BROWSER visiting URL: " + str(BASE_URL)
    browser.visit(BASE_URL)

    # Keep scrolling down until we've reached the right league
    for i in range(1, 100000):
        # Scroll to bottom of page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait 1 second
        time.sleep(1)
        # Find and click "See More" button if it exists
        click_see_more_btn(browser, numSummoners)
        # Wait 1 second
        time.sleep(1)

    return browser

numAttempts = 0
btnFound = False
def click_see_more_btn(browser, numSummoners):
    global numAttempts
    global btnFound

    # Find the button with the id "moreLadderRakingTable"
    if numAttempts < 4:
        try:
            # NOTE: op.gg has a typo in the button id, Raking NOT Ranking
            button = browser.find_by_id('moreLadderRakingTable')
            button.click()
            numAttempts = 0  #Reset num attempts
            btnFound = True
            check_ranking(browser, numSummoners)
        except Exception:
            btnFound = False
            print "ERR: See More button NOT found."

    if not btnFound:
        # Try again
        numAttempts += 1
        click_see_more_btn(browser, numSummoners)

loSummonerNames = []
def check_ranking(browser, numSummoners):

    try:
        # Find every summoner on the current page by xpath
        #xpath = '//td[@class="SummonerName"]'
        xpath = '//tr[@class]'
        summoners = browser.find_by_xpath(xpath)

        # Check the LAST summoner on the current page to see if it's in Plat or Gold. This is
        #  a hack to quickly figure out if we can get lots of summoners of desired rank
        last_summoner_league = summoners[-1].text.split('\n')[2]
        if 'Platinum' in last_summoner_league or 'Gold' in last_summoner_league:
            print 'Acceptable Rank Found in Last Element.'
            # If the LAST summoner is good, check the rest of the the page

            for summoner in summoners:
                split_summoner = summoner.text.split('\n')
                #rank = split_summoner[0]
                summoner_name = split_summoner[1]
                league = split_summoner[2]
                if 'Platinum' in str(league) or 'Gold' in str(league):
                    print "Acceptable league found"
                    if (numSummoners > len(loSummonerNames)):
                        print "Appended summoner " + summoner_name
                        write_summoner_name(summoner_name)
                    else:
                        print "DONE: " + str(len(loSummonerNames)) + " summoners found."
                        sys.exit(0)
                else:
                    print "League not acceptable"
    except Exception:
        print "ERR: Rank NOT found."


def write_summoner_name(summoner_name):
    file = open(os.curdir+"_out_opgg_summonerNames.txt", 'a')
    file.writelines(str(summoner_name)+"\n")


'''
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
'''

if __name__ == "__main__":
    main()