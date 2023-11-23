import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Random;

public class HogSimulator {
    private int type;
    private int winScore;
    private int maxDice;
    private Random random;
    private BufferedReader stdIn;
    public static void main(String[] args) throws IOException {
        HogSimulator game = new HogSimulator(0, 100, 10);
        game.runGame();
    }
    public HogSimulator(int type, int winScore, int maxDice) {
        this.type = type;
        this.winScore = winScore;
        this.maxDice = maxDice;
        this.random = new Random();
        this.stdIn = new BufferedReader(new InputStreamReader(System.in));
    }

    public void runGame() throws IOException {
        int turn = 0;
        int score0 = 0;
        int score1 = 0;
        int numRolls;
        boolean gameOver = false;
        while (!gameOver) {
            if (turn == 0) {
                numRolls = promptInput(score0, score1, type / 2, 1);
                score0 = computeScore(numRolls, score0, score1, 1);
                if (score0 >= winScore) {
                    System.out.println("Player 1 wins!");
                    gameOver = true;
                }
                turn = 1;
            } else {
                numRolls = promptInput(score1, score0, type % 2, 2);
                score1 = computeScore(numRolls, score1, score0, 2);
                if (score1 >= winScore) {
                    System.out.println("Player 2 wins!");
                    gameOver = true;
                }
                turn = 0;
            }
        }
    }
    public int promptInput(int myScore, int otherScore, int isComputer, int playerNum) throws IOException {
        if (isComputer == 0) {
            System.out.println("Player " + playerNum + ", the score is " + myScore + " to " + otherScore + ". How many dice would you like to roll? (0-" + maxDice + ")");
            String response;
            int toReturn;
            while (true) {
                response = stdIn.readLine();
                try {
                    toReturn = Integer.parseInt(response);
                } catch (Exception e) {
                    System.out.println("Not an integer.");
                    continue;
                }
                if (toReturn < 0 || toReturn > maxDice) {
                    System.out.println("Not in range.");
                } else {
                    break;
                }
            }
            return toReturn;
        } else {
            return 0;
        }
    }
    public int[] rollDice(int numRolls) {
        int[] toReturn = new int[numRolls];
        for (int i = 0; i < numRolls; i++) {
            toReturn[i] = random.nextInt(1, 7);
        }
        return toReturn;
    }
    public int zeroRoll(int otherScore) {
        return 2 * Math.abs((otherScore / 10) % 10 - otherScore % 10) + 1;
    }
    public boolean isPerfectSquare(int num) {
        int sqrt = (int) Math.sqrt(num);
        return (sqrt * sqrt == num);
    }
    public int computeScore(int numRolls, int myScore, int otherScore, int playerNum) {
        int toAdd;
        if (numRolls == 0) {
            toAdd = zeroRoll(otherScore);
            System.out.println("Player " + playerNum + " rolls 0 dice and gets 2*|" + (otherScore / 10 % 10) + "-" + (otherScore % 10) + "|+1 = " + toAdd + " points!");
        } else {
            int[] rolls = rollDice(numRolls);
            toAdd = 0;
            for (int i : rolls) {
                if (i == 1) {
                    toAdd = 1;
                    break;
                } else {
                    toAdd += i;
                }
            }
            if (toAdd == 1) {
                System.out.println("Player " + playerNum + " rolls " + numRolls + " dice and gets " + Arrays.toString(rolls) + ", giving " + toAdd + " point!");
            } else {
                System.out.println("Player " + playerNum + " rolls " + numRolls + " dice and gets " + Arrays.toString(rolls) + ", giving " + toAdd + " points!");
            }
        }
        int sqrt = (int) Math.sqrt(myScore + toAdd);
        if (sqrt * sqrt == myScore + toAdd) {
            int newScore = (sqrt + 1) * (sqrt + 1);
            System.out.println(myScore + " + " + toAdd + " = " + (myScore + toAdd) + " is a perfect square, so Player " + playerNum + "'s score is now " + newScore + "!");
            return newScore;
        } else {
            System.out.println("Player " + playerNum + "'s score is now " + myScore + " + " + toAdd + " = " + (myScore + toAdd) + "!");
            return myScore + toAdd;
        }

    }
}