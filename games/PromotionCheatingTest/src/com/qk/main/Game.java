package com.qk.main;

import java.util.Random;

/*
 * This is a simple code to test the optimal betting strategies for players:
 * If given a free bonus, player are not allowed to cash out the free bonus until his total bet
 * reaches (N x bonus).
 * This is a simplified game (coin game), where the player have 50% chance to win $1.95 back and
 * 50% chance to get nothing for every dollar he bets.
 */

public class Game {
	
	private static double bonus = 1;
	private static double minBet[] = {0.1,0.2,0.5,1};
	private static double minWager[] = {1,2,5,10,50,100,500,1000};
	//private static double minBet[] = {0.1};
	//private static double minWager[] = {1};
	private static int numSim = 1000000;
	private static double odds = 1.95;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Survival Rate");
		Random rand = new Random();
		for(int i=0; i<minBet.length; i++){
			double bet = minBet[i];
			for(int j=0; j<minWager.length; j++){
				double wager = minWager[j];
				
				int countSurvival = 0;
				double totalReturn = 0;
				for(int k=0; k<numSim; k++){
					double cumWager = 0;
					double money = bonus*1.0;
					while((cumWager<wager) && (money>=bet)){
						double r = rand.nextDouble();
						//System.out.println(r);
						money -= bet;
						cumWager += bet;
						if(r>0.5){
							money += (odds*bet);
						}						
					}
					
					//System.out.println(cumWager+";"+money);
					if((cumWager+1e-9)>=wager){
						countSurvival += 1;
						totalReturn += money;
					}
				}
				double survivalRate = countSurvival*1.0/numSim;
				double returnRate = totalReturn/(numSim*bonus);
				//System.out.println(countSurvival);
				System.out.println("bet "+bet+"; minWager "+wager+": "+survivalRate+"  "+returnRate);
				
				
			}
			
		}
		
	}

}
