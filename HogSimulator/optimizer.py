from math import comb
from decimal import *
import sys


def all_possible(n):
    assert type(n)==int and 1<=n<=10
    probs = [0]*(6*n)
    probs[0] = (Decimal(1)-Decimal(5**n)/Decimal(6**n))
    for i in range(0, (4*n)+1):
        i_prob = Decimal(0)
        for j in range(0, i//5+1):
            i_prob += (-1)**j * comb(n, j) * comb((n-1) + i - 5*j, (n-1))
        i_prob /= Decimal(6**n)
        probs[(2*n-1)+i] = i_prob
    return probs

def next_square(n):
    assert type(n) == int
    squart = n**0.5
    if (squart%1)==0:
        return int((squart+1)**2)
    else:
        return n

def tail_points(opponent_score):
    return 2*abs((opponent_score//10)%10 - opponent_score%10)+1

def p(x, y, accuracy = 2):
    print('Win chance: ' + str(round(prob_grid[x][y]*100, accuracy)) + '%')
def m(x, y):
    print ('Best move: ' + str(move_grid[x][y]))
def pm(x, y, accuracy = 2):
    print('Win chance: ' + str(round(prob_grid[x][y]*100, accuracy)) + '%')
    print('Best move: ' + str(move_grid[x][y]))

win_score = 100
max_dice = 10
precision = 20

if (len(sys.argv) > 1):
    win_score = int(sys.argv[1])
if (len(sys.argv) > 2):
    max_dice = int(sys.argv[2])
if (len(sys.argv) > 3):
    precision = int(sys.argv[3])

getcontext().prec = precision

poss_list = [all_possible(i) for i in range(1, max_dice + 1)]

prob_grid = []
for i in range(win_score):
    prob_grid.append([0]*win_score)
move_grid = [[0]*win_score for i in range(win_score)]


prob_grid[win_score - 1][win_score - 1] = Decimal(1)

for i in range(2, 2*win_score):
    for j in range(max(0, i-win_score), min(win_score, i)):
        x = win_score-1-((i-1)-j) #player score
        y = win_score-1-j #opponent score
        done = False
        current_max = Decimal(0)
        current_rolls = 0
        if next_square(x + tail_points(y)) >= win_score: #returns 1 if score goes over win_score
            current_max = 1
            done = True
        else:
            current_max = 1 - prob_grid[y][next_square(x + tail_points(y))] #prob from 0 rolls
        if current_max==1:
            done = True
        r = 0
        while r < max_dice and done == False:
            total_prob = Decimal(0)
            if next_square(x+1) >= win_score:
                total_prob += 1 * poss_list[r][0]
            else:
                total_prob += (1-prob_grid[y][next_square(x+1)]) * poss_list[r][0]
            for roll in range(2*(r+1), 6*(r+1)+1): #remember to subtract 1 for indices
                if next_square(x + roll) >= win_score:
                    total_prob += 1 * poss_list[r][roll-1]
                else: 
                    total_prob += (1 - prob_grid[y][next_square(x + roll)]) * poss_list[r][roll-1]
            if total_prob > current_max:
                current_max = total_prob
                current_rolls = r+1
            if current_max == 1:
                done = True
            r += 1
        prob_grid[x][y] = current_max
        move_grid[x][y] = current_rolls

f = open('opt_moves.txt', 'w')
f.writelines([str(lst)[1:-1] + '\n' for lst in move_grid])
f.close()
#print(prob_grid)
#print(move_grid)

