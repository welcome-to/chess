from decode import decode_game

import sys


if __name__ == "__main__":
    f = open('1800plus.txt')
    gamenumber = 0
    for lines in f:
        if gamenumber%10000 == 0:
            #print(gamenumber)
            pass
        if lines[0:2] == '1.':
            gamenumber += 1
            try:
                print("Game {0}".format(gamenumber), file=sys.stderr)
                game = decode_game(lines)
                gamefile = open('gamebase/game{0}'.format(gamenumber),'w')
                gamefile.write('\n')
                for i in game:
                    gamefile.write('\n'+str(i))
                gamefile.close()
            except Exception as ex:
                print("Game {0}: exception. {1}\nGame:{2}".format(gamenumber, ex, lines))

    f.close()
