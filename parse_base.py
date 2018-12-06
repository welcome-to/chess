from decode import decode_game

from datetime import datetime
from multiprocessing import Process
import sys


DATE_FORMAT = "%d.%m.%Y"




def parse(filename,proces_id):
    f = open(filename)
    gamenumber = 0
    players_line = ''
    date_line = ''
    for lines in f:
        if gamenumber%10000 == 0:
            #print(gamenumber)
            pass
        if lines[0:2] == '1.':
            gamenumber += 1
            try:
                print("Game {0}".format(gamenumber), file=sys.stderr)
                game = decode_game(lines)
                gamefile = open('gamebase/game_{0}_{1}'.format(proces_id,gamenumber),'w')
                gamefile.write('\n')
                for i in game:
                    gamefile.write('\n'+str(i))
                gamefile.close()
            except Exception as ex:
                print(players_line + date_line + "Game {0}: exception. {1}\n{2}".format(gamenumber, ex, lines))
        elif lines.strip() and lines.strip()[-1] == ']':
            players_line = lines
            #print ("Players line: " + players_line + "," + lines)
        else:
            if not lines.strip():
                continue
            last_word = lines.strip().split(' ')[-1]
            try:
                _ = datetime.strptime(last_word, DATE_FORMAT)
                date_line = lines
            except:
                pass

    f.close()


def parse_conrtoler(filename,proceses):
    f = open(filename)
    a=0
    for lines in f:
        a+=1
    f.close()
    lines = a
    lines_in_file = lines//proceses
    f = open(filename)
    for i in range(proceses):
        out = open('to_parse/out_{0}'.format(i+1),'w')
        for j in range(lines_in_file):
            out.write(f.readline())
        out.close()
    out = open('to_parse/out_{0}'.format(proceses),'w')
    for i in range(lines%proceses):
        out.write(f.readline())
    out.close()
    for i in range(proceses):
        Process(target=parse,args = ('to_parse/out_{0}'.format(i+1),i+1)).start()



if __name__ == "__main__":
    inputfile = input('Input file name: ')
    parse_conrtoler(inputfile,int(input('Input count of processes: ')))