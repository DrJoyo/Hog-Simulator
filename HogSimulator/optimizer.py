from math import comb
from decimal import *
import sys

# Calculates the probability distribution of the score from rolling n dice using generating functions
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

# Returns the next perfect square if n is a perfect square, or just n otherwise
def next_square(n):
    assert type(n) == int
    sqrt = n**0.5
    if (sqrt%1)==0:
        return int((sqrt+1)**2)
    else:
        return n

# Calculates the number of points scored by rolling 0 dice given the opponent's score
def zero_dice_points(opponent_score):
    return 2*abs((opponent_score//10)%10 - opponent_score%10)+1

# Functions to access data in interactive mode, for debugging or finding optimal play in game
def p(x, y, accuracy = 2):
    print('Win chance: ' + str(round(prob_grid[x][y]*100, accuracy)) + '%')
def m(x, y):
    print ('Best move: ' + str(move_grid[x][y]))
def pm(x, y, accuracy = 2):
    print('Win chance: ' + str(round(prob_grid[x][y]*100, accuracy)) + '%')
    print('Best move: ' + str(move_grid[x][y]))

# Set default values
win_score = 100
max_dice = 10
precision = 20
write_file = 'opt_moves.txt'

# Take arguments
if (len(sys.argv) > 1):
    win_score = int(sys.argv[1])
if (len(sys.argv) > 2):
    max_dice = int(sys.argv[2])
if (len(sys.argv) > 3):
    precision = int(sys.argv[3])
if (len(sys.argv) > 4):
    write_file = sys.argv[4]

# Set precision of Decimal calculations
getcontext().prec = precision

# Calculate probability distributions of score for all legal numbers of rolls
poss_list = [all_possible(i) for i in range(1, max_dice + 1)]

# Create arrays for dynamic programming
prob_grid = [[0]*win_score for i in range(win_score)]
move_grid = [[0]*win_score for i in range(win_score)]

# Base case
prob_grid[win_score - 1][win_score - 1] = Decimal(1)
move_grid[win_score - 1][win_score - 1] = 0

# Recursive algorithm, called on diagonals 
for i in range(2, 2*win_score):
    for j in range(max(0, i-win_score), min(win_score, i)):
        x = win_score-1-((i-1)-j) # player score
        y = win_score-1-j # opponent score
        done = False
        current_max_prob = Decimal(0)
        current_max_rolls = 0
        if next_square(x + zero_dice_points(y)) >= win_score: # returns probability 1 if score goes over win_score
            current_max_prob = 1
            done = True
        else:
            current_max_prob = 1 - prob_grid[y][next_square(x + zero_dice_points(y))] # probability of winning after 0 rolls
        if current_max_prob==1:
            done = True
        roll_num = 1 # Number of rolls
        while roll_num <= max_dice and done == False: # Compare expected probability of winning after all positive dice roll #'s
            total_prob = Decimal(0)
            if next_square(x+1) >= win_score:
                total_prob += 1 * poss_list[roll_num-1][0]
            else:
                total_prob += (1-prob_grid[y][next_square(x+1)]) * poss_list[roll_num-1][0]
            for score in range(2*roll_num, 6*roll_num+1): # For all possible scores after rolling
                if next_square(x + score) >= win_score:
                    total_prob += 1 * poss_list[roll_num-1][score-1]
                else: 
                    total_prob += (1 - prob_grid[y][next_square(x + score)]) * poss_list[roll_num-1][score-1]
            if total_prob > current_max_prob: # Compare expected probability to current best
                current_max_prob = total_prob
                current_max_rolls = roll_num
            if current_max_prob == 1: # Exit early if expected probability is 1
                done = True
            roll_num += 1
        prob_grid[x][y] = current_max_prob
        move_grid[x][y] = current_max_rolls

# Write optimal moves to the specified text file (opt_moves.txt by default)
f = open(write_file, 'w')
f.writelines([str(lst)[1:-1] + '\n' for lst in move_grid])
f.close()

