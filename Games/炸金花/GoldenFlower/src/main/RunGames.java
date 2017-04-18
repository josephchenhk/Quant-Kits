package main;

import java.util.ArrayList;
import game.TenThousandGame;
import game.DragonPhoenix;

public class RunGames {
	
	private static int NUMSIM = 20000;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		/*
		System.out.println("ը�𻨣��f�ˈ�");
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
		
		
		System.out.println("ը�𻨣����P���Q");
		double totalPay = 0;
		double totalRec = 0; 
		for (int i=0; i<NUMSIM; i++){
			DragonPhoenix game2 = new DragonPhoenix();
			
			//bet player
			String[] betPlayer = {}; //{"dragon"};
			double[] betAmount = {}; //{1};			
			for (int j=0; j<betAmount.length; j++){
				totalPay += betAmount[j];
			}		
		    double pay = game2.WinBet(betPlayer, betAmount);
		    System.out.println("Pay:"+pay);
		    totalRec += pay;
		    
		    //bet type
		    String[] betType = {"pair"};
			double[] betTypeAmount = {1}; 
		    for (int j=0; j<betTypeAmount.length; j++){
				totalPay += betTypeAmount[j];
			} 
		    double pay2 = game2.TypeBet(betType, betTypeAmount);
		    System.out.println("Pay2:"+pay2);
		    totalRec += pay2;
		}
		System.out.println("Total Pay: "+totalPay);
		System.out.println("Total Receive: "+totalRec);
		System.out.println("RTP: "+(totalRec*1.0/totalPay));
		
	}

}
