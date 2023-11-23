import java.io.*;
import java.util.Arrays;
import java.util.Random;

public class HogSimulator {
    private int type;
    private int winScore;
    private int maxDice;
    private Random random;
    private String fileName;
    private int[][] optimalMoves;
    private BufferedReader stdIn;
    public static void main(String[] args) throws IOException {
        HogSimulator game;
        switch (args.length) {
            case 0:
                game = new HogSimulator(100, 10, 1, "opt_moves.txt");
                break;
            case 1:
                game = new HogSimulator(Integer.parseInt(args[0]), 10, 1, "opt_moves.txt");
                break;
            case 2:
                game = new HogSimulator(Integer.parseInt(args[0]), Integer.parseInt(args[1]), 1, "opt_moves.txt");
                break;
            case 3:
                game = new HogSimulator(Integer.parseInt(args[0]), Integer.parseInt(args[1]), Integer.parseInt(args[2]), "opt_moves.txt");
                break;
            default:
                game = new HogSimulator(Integer.parseInt(args[0]), Integer.parseInt(args[1]), Integer.parseInt(args[2]), args[3]);
                break;
        }
        game.runGame();
    }
    public HogSimulator(int winScore, int maxDice, int type, String fileName) throws IOException {
        this.type = type;
        this.winScore = winScore;
        this.maxDice = maxDice;
        this.random = new Random();
        this.stdIn = new BufferedReader(new InputStreamReader(System.in));
        this.fileName = fileName;
        if (type > 0) {
            this.optimalMoves = readOptimalMoves();
        }
    }
    /** Reads optimal moves from the specified file */
    public int[][] readOptimalMoves() throws IOException {
        int[][] toReturn = new int[winScore][winScore];
        BufferedReader fileReader = new BufferedReader(new FileReader(fileName));
        for (int i = 0; i < winScore; i++) {
            String line = fileReader.readLine();
            String[] split = line.split(", ");
            if (split.length != winScore) {
                throw new IllegalStateException(fileName + " dimensions do not match input");
            }
            for (int j = 0; j < winScore; j++) {
                toReturn[i][j] = Integer.parseInt(split[j]);
            }
        }
        if (fileReader.readLine() != null) {
            throw new IllegalStateException(fileName + " dimensions do not match input");
        }
        return toReturn;
    }
    /** Simulates a game between two players */
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

    /** Tells the player to type in a number or returns the computer's optimal play */
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
            return optimalMoves[myScore][otherScore];
        }
    }
    /** Computes the new score after rolling numRolls times */
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

    /** Simulates numRolls dice rolls and returns the array of rolls */
    public int[] rollDice(int numRolls) {
        int[] toReturn = new int[numRolls];
        for (int i = 0; i < numRolls; i++) {
            toReturn[i] = random.nextInt(1, 7);
        }
        return toReturn;
    }
    /** Returns score from rolling zero dice */
    public int zeroRoll(int otherScore) {
        return 2 * Math.abs((otherScore / 10) % 10 - otherScore % 10) + 1;
    }
    /** Checks if a number is a perfect square */
    public boolean isPerfectSquare(int num) {
        int sqrt = (int) Math.sqrt(num);
        return (sqrt * sqrt == num);
    }

}