__author__ = 'Deniz'

import re

def main():
    f = open('opgg.txt', 'r')
    lines = f.readlines()


    start = ','
    end = "Platinum"

    summoner_names = []

    try:
        result = re.findall("%s(.*)%s" % (start, end), str(lines))

        results_array = str(result).split("', '")

        for r in results_array:
            if r.__contains__('Platinum') or r.__contains__('Diamond') or r.__contains__(","):
                pass
            elif r[:3] == r"\\n":
                pass
            elif r.__contains__(r'\\x'):
                pass
            else:
                summoner_names.append(r[1:-3])
                print r[1:-3]

    except AttributeError:
        print "ERR: Data Not Found."

    f = open('_out_opgg.txt', 'a')

    for summoner in summoner_names:
        summoner = str(summoner).replace(' ', '')
        f.write(str(summoner).lower()+"\n")


if __name__ == "__main__":
    main()