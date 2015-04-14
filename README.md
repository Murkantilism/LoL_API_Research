LoL API Research
================

A Northeastern University research project studying the effects of perceived gender on League of Legends player behavior via Riot's official API.

## Goal
To study League of Legends statistical data and search for a correlation or connection between player behavior and perceived gender.

## Programmer's Disclaimer

The code in this repository is a bird's nest. Even looking through the commit history of this README will give a glimpse at the rapidly changing requirements of this research project. Because of how often the requirements of the project changed, it was difficult to write a proper piece of software. 8 months ago, had I known this, I might have been able to architect a better code base. But alas, each time the requirements changed (a total of 5-6 times) I ended up writing a slew of new scripts and deprecating several old ones. Thus is the tale of a 2nd semester senior with few hours to spare each week.

To those looking to use this repository, I wish you the best of luck. It's not amazingly well documented nor organized, and likely riddled with dozens of bugs. One day I hope to go through and clean out this repo, maybe even rewriting everything into a single usable tool. For now, this is best used an an example, but attempting to use these scripts yourself may be fruitless.

## Overview
We gathered a large data set of summoner and match history data via [RiotWatcher (a Python wrapper)](https://github.com/pseudonym117/Riot-Watcher) and Riot's developer API.

The first step in collecting our data was identifying summoners that met our Gold or Platinum league requirements. This was done by scraping third-party website op.gg's rankings page, which lists every active player by league and also provides a close approximation to the MMR scores. Please note that Riot does not disclose summoners’ MMR score nor explains how it is calculated except mentioning that it is based only on wins and losses. 

With approximately 2,000 in the control group and 100 in the experimental, we used the Riot API in tandem with the RiotWatcher Python wrapper to get the summoner ID, match history, match data, and most used champion for each summoner for the last 15 games played. All of this data was accessed from several endpoints in the API, however this does not give us the complete picture of information we need. 

In order to compare players of relatively similar skill levels, we had to approximate their Match Making Rating (MMR), since Riot does not publicly disclose how they compute MMRs in-game. We once again scraped op.gg, but this time used a Selenium driver called Splinter to search by summoner name and get details on their MMR and the average MMR of the league they are in, as approximated by op.gg's algorithm. 

Once all of this data was collected, we parsed and formatted it into CSV files, ready for slicing into bins and analysis. During the data collection and processing, dozens of summoners had missing or incomplete data and had to be thrown out from the study.

##Collaborators:
Deniz Ozkaynak

Alessandro Canossa

Emma Witkowski

Zhengxing Chen

Truong-Huy Nguyen

Christoffer Holmgård

## CHI PLAY
We are aiming to have research finished in time to submit a paper to the upcoming 2015 CHI PLAY conference.

![Northeastern CAMD](https://raw.github.com/Murkantilism/LoL_API_Research/dev/Screens/camd.png)
![League of Legends](https://raw.github.com/Murkantilism/LoL_API_Research/dev/Screens/lol.png)
![CHI PLAY](https://raw.github.com/Murkantilism/LoL_API_Research/dev/Screens/chiplay.png)
