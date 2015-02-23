__author__ = 'Deniz'

def main():
    f = open('_out_opgg_most_used_summoners.txt', 'r')
    read_input = f.readlines()

    g = open('_out_opgg_most_used_summoners_reformatted.txt', 'a')

    for line in read_input:
        splitlines = line.split(":")
        #print splitlines
        new_format = str(str(splitlines[0])+":"+str(splitlines[1]+"="+str(splitlines[2])))
        g.write(new_format)


if __name__ == "__main__":
    main()