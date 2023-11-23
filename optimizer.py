from math import comb
from decimal import *
getcontext().prec = 100

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

poss_list = [all_possible(1), all_possible(2), all_possible(3), all_possible(4), all_possible(5), all_possible(6), all_possible(7), all_possible(8), all_possible(9), all_possible(10)]

prob_grid = []
for i in range(100):
    prob_grid.append([0]*100)
move_grid = [[0]*100 for i in range(100)]


prob_grid[99][99] = Decimal(1)
#for i in range(100):
    #prob_grid[99][i] = 1
    #move_grid[99][i] = 0 
#for i in range(2, 6):

for i in range(2, 200):
    for j in range(max(0, i-100), min(100, i)):
        x = 99-((i-1)-j) #player score
        y = 99-j #opponent score
        done = False
        current_max = Decimal(0)
        current_rolls = 0
        if next_square(x + tail_points(y)) >= 100: #returns 1 if score goes over 100
            current_max = 1
            done = True
        else:
            current_max = 1 - prob_grid[y][next_square(x + tail_points(y))] #prob from 0 rolls
        if current_max==1:
            done = True
        r = 0
        while r < 10 and done == False:
            total_prob = Decimal(0)
            if next_square(x+1) >= 100:
                total_prob += 1 * poss_list[r][0]
            else:
                total_prob += (1-prob_grid[y][next_square(x+1)]) * poss_list[r][0]
            for roll in range(2*(r+1), 6*(r+1)+1): #remember to subtract 1 for indices
                if next_square(x + roll) >= 100:
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

print(prob_grid)
print(move_grid)

def p(x, y, accuracy = 2):
    print('Win chance: ' + str(round(prob_grid[x][y]*100, accuracy)) + '%')
def m(x, y):
    print ('Best move: ' + str(move_grid[x][y]))
def pm(x, y, accuracy = 2):
    print('Win chance: ' + str(round(prob_grid[x][y]*100, accuracy)) + '%')
    print('Best move: ' + str(move_grid[x][y]))