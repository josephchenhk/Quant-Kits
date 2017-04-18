package main;

import java.util.ArrayList;
import game.TenThousandGame;
import game.DragonPhoenix;

public class RunGames {
	
	private static int NUMSIM = 20000000;
	private static int NUMGAME = 6; // number of games per deck

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		/*
		System.out.println("炸金花：萬人場");
		int totalPay = 0;
		int totalRec = 0; 
		for (int i=0; i<NUMSIM; i++){
			TenThousandGame game1 = new TenThousandGame();
			//String[] betPlayer = {"player1","player2"};
			//int[] betAmount = {1,1};
			String[] betPlayer = {"player1"};
			int[] betAmount = {1};
			for (int j=0; j<betAmount.length; j++){
				totalPay += betAmount[j];
			}
		    int pay = game1.Bet(betPlayer, betAmount);
		    System.out.println("Pay:"+pay);
		    totalRec += pay;
		}
		System.out.println("Total Pay: "+totalPay);
		System.out.println("Total Receive: "+totalRec);
		System.out.println("RTP: "+(totalRec*1.0/totalPay));
		*/
		
		long startTime = System.nanoTime();
		System.out.println("炸金花：龍鳳對決");
		double totalPay = 0;
		double totalRec = 0; 
		DragonPhoenix game2 = new DragonPhoenix();
		for (int i=0; i<NUMSIM; i++){
			if (i%NUMGAME==0){
				//System.out.println(i);
				game2 = new DragonPhoenix();
			}else{
				game2.StartNewGame();
			}
			
			
			//bet player
			String[] betPlayer = {"phoenix"}; //{"dragon","phoenix"};
			double[] betAmount = {1}; //{1};			
			for (int j=0; j<betAmount.length; j++){
				totalPay += betAmount[j];
			}		
		    double pay = game2.WinBet(betPlayer, betAmount);
		    //System.out.println("Pay *:"+pay);
		    totalRec += pay;
		    
		    //bet type
		    String[] betType = {}; //{"pair8","flush","straight","straightFlush","leopard"};
			double[] betTypeAmount = {}; 
		    for (int j=0; j<betTypeAmount.length; j++){
				totalPay += betTypeAmount[j];
			} 
		    double pay2 = game2.TypeBet(betType, betTypeAmount);
		    //System.out.println("Pay2 **:"+pay2);
		    totalRec += pay2;
		}
		System.out.println("Total Pay: "+totalPay);
		System.out.println("Total Receive: "+totalRec);
		System.out.println("RTP: "+(totalRec*1.0/totalPay));
		long estimatedTime = System.nanoTime() - startTime;
		System.out.println("Elapsed Time: "+estimatedTime/(Math.pow(10, 9))+" seconds.");
		
	}

}
