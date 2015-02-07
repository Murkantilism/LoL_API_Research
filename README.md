LoL API Research
================

A Northeastern University research project studying the effects of perceived gender on League of Legends player behavior via Riot's official API.

## Goal
To study League of Legends statistical data and search for a corellation or connection between player behavior and perceived gender.

## Overview
We gathered a large data set of summoner and match history data via [RiotWatcher (a Python wrapper)](https://github.com/pseudonym117/Riot-Watcher) and Riot's developer API. Now we are in the process of building three statistical prediction models:

1. A model based on win/loss history (mimicing Riot's internal ELO ranking)
2. A model based on summoner actions in actual matches, calculating a "match score" with an ML algorithm assigning each action an importance value
3. A model based on summoner actions in actual matches, calculating a "match score" with expert League of Legends players assigning each action a more subjective importance value

Looking at the results of these 3 prediction models, we can accurately predict if a given summoner will win versus another, and then look at their gender and how they percieve the gender of other summoners, and search for any correlation affecting their behavior, performance, and skill.

##Collaborators:
Deniz Ozkaynak

Alessandro Canossa

Christoffer Holmgård

Zhengxing Chen

## CHI PLAY
We are aiming to have research finished in time to submit a paper to the upcoming 2015 CHI PLAY conference.

![Northeastern CAMD](https://raw.github.com/Murkantilism/LoL_API_Research/dev/Screens/camd.png)
![League of Legends](https://raw.github.com/Murkantilism/LoL_API_Research/dev/Screens/lol.png)
![CHI PLAY](https://raw.github.com/Murkantilism/LoL_API_Research/dev/Screens/chiplay.png)
